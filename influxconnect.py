import influxdb_client
from settings.settings import mysettings


# Store the URL of your InfluxDB instance
url = f"http://{mysettings.INFLUXDB_IP}:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=mysettings.INFLUXDB_TOKEN,
    org=mysettings.INFLUXDB_TOKEN
)

# Query script
query_api = client.query_api()
query = f'from(bucket:"{mysettings.INFLUXDB_BUCKET}")\
  |> range(start: -1m)\
  |> filter(fn: (r) => r["_measurement"] == "battery")\
  |> filter(fn: (r) => r["_field"] == "Energy.Battery.Charge.Level")\
  |> filter(fn: (r) => r["unit"] == "Percent")\
  |> min()'
result = query_api.query(org=mysettings.INFLUXDB_ORG, query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), record.get_value()))

print(results)
