from flask import Flask, render_template, request, redirect, url_for, make_response
import RPi.GPIO as GPIO
from influxconnect import querylib, queryinfluxdb

pin1 = 32  # Relais Pins Nummer
pin2 = 16

GPIO.setmode(GPIO.BOARD)  # GPIO MODE

GPIO.setup(pin1, GPIO.OUT)  # Alle Relais Pins als OUTPUT
GPIO.setup(pin2, GPIO.OUT)

GPIO.output(pin1, 1)
GPIO.output(pin2, 1)

app = Flask(__name__)  # Flask Server einrichten

def getFirstValue(array):
    try:
        return array[0][1]
    except:
        return None


# Rückgabe der Seite index.html wenn die IP-Adresse ausgewählt ist

@app.route('/')
def index():
    result = queryinfluxdb(querylib.BATTERY_CHARGE)
    return render_template('index.html', charge=getFirstValue(result))


# Jeder HTML-Taster ergibt einen Nummer zurück

@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):
    changePin = int(changepin)  # cast changepin to an int

    if changePin == 1:
        print("Boiler AN")  # Relais1 AN
        GPIO.output(pin1, 0)  # Low-Pegel

    elif changePin == 2:
        print("Heizung")  # Relais2 AN
        GPIO.output(pin2, 0)

    else:
        print("Boiler AUS")  # Alle Relais AUS
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 1)

    response = make_response(redirect(url_for('index')))

    return (response)


app.run(debug=True, host='0.0.0.0', port=8000)  # Einrichten des Servers im Debug-Modus für Port 8000
