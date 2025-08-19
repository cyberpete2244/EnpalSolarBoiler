from influxconnect import querylib, queryinfluxdb


def getFirstValue(array):
    try:
        return array[0][1]
    except:
        return None

def run():
    result = queryinfluxdb(querylib.BATTERY_CHARGE)
    print(getFirstValue(result))


if __name__ == '__main__':
    run()
