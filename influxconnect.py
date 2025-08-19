import influxdb_client
import settings


mysettings = settings.Settings()


client = influxdb_client.InfluxDBClient(
    url=f"http://{mysettings.INFLUXDB_IP}:8086",
    token=mysettings.INFLUXDB_TOKEN,
    org=mysettings.INFLUXDB_TOKEN
)

# Query script
query_api = client.query_api()


class QueryLib:
    BATTERY_CHARGE = f'from(bucket:"{mysettings.INFLUXDB_BUCKET}")\
      |> range(start: -10m)\
      |> filter(fn: (r) => r["_measurement"] == "battery")\
      |> filter(fn: (r) => r["_field"] == "Energy.Battery.Charge.Level")\
      |> filter(fn: (r) => r["unit"] == "Percent")\
      |> distinct()\
      |> yield(name: "distinct")'


querylib = QueryLib()


def queryinfluxdb(query):
    result = query_api.query(org=mysettings.INFLUXDB_ORG, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    return results
