from requests import get
import pandas as pd
import os, signal
import board
import adafruit_dht
import RPi.GPIO as GPIO
import time
import datetime
from datetime import date
import MySQLdb
from w1thermsensor import W1ThermSensor

CONST_DATOANIO = 525600
CONST_DATOMES = 43200
CONST_DATOSEMANA = 10080
CONST_DATODIA = 1440


class Sensor:
    def __init__(self, id, codigo):
        self.id = id
        self.codigo = codigo


class DHT(Sensor):
    def __init__(self, id, codigo):
        self.humedad = None
        self.temp = None
        self.temperaturas = [None]
        self.humedades = [None]

        Sensor.__init__(self, id, codigo)

        self.device = adafruit_dht.DHT22(codigo, use_pulseio=True)

    def leerdatos(self):
        try:
            self.temp = self.device.temperature
            self.humedad = self.device.humidity
            self.temperaturas.append(round(self.temp, 1))
            self.humedades.append(round(self.humedad))
        except RuntimeError as error:
            pass
        except Exception as error:
            pass

    def getDatos(self):
        datos = []
        modaT = max(self.temperaturas, key=self.temperaturas.count)
        modaH = max(self.humedades, key=self.humedades.count)
        datos.append(modaT)
        datos.append(modaH)
        self.temperaturas = [modaT]
        self.humedades = [modaH]
        return datos

    def mostrarDatos(self):
        print("Sensor Numero: ", self.id, " Codigo de sensor: "
              , self.codigo, " Temperatura del sensor: ", self.temp
              , " Humedad del sensor: ", self.humedad)

    def reiniciarTablas(self):
        self.temperaturas = []
        self.humedades = []


class DS(Sensor):
    def __init__(self, id, codigo):
        Sensor.__init__(self, id, codigo)
        self.temp = None
        self.temperaturas = [None]

    def leerdatos(self):
        try:
            for sensor in W1ThermSensor.get_available_sensors():
                if sensor.id == self.codigo:  # sensor 8
                    self.temp = sensor.get_temperature()
            self.temperaturas.append(round(self.temp, 1))
        except:
            pass

    def getDatos(self):
        moda = max(self.temperaturas, key=self.temperaturas.count)
        self.temperaturas = [moda]
        return moda

    def mostrarDatos(self):
        print("Sensor Numero: ", self.id, " Codigo de sensor: "
              , self.codigo, " Temperatura del sensor: ", self.temp)

    def reiniciarTablas(self):
        self.temperaturas = []


class Camara:
    def __init__(self, id):
        self.id = id
        self.tam = 0
        self.sensores = []

    def agregarSensor(self, sensor):
        self.tam += 1
        self.sensores.append(sensor)

    def getDatos(self):
        return self.sensores

    def mostrarSensores(self):
        for i in range(len(self.sensores)):
            self.sensores[i].mostrarDatos()

    def getTam(self):
        return self.tam

    def reiniciarTabla(self):
        for i in range(len(self.sensores)):
            self.sensores[i].reiniciarTablas()


db2 = MySQLdb.connect(host="bt5oimjjyou8twabxrxj-mysql.services.clever-cloud.com", user="ucsdioytffgjrvnf",
                      passwd="8wzDXU0L1nApbdR6FcSn", db="bt5oimjjyou8twabxrxj")
cur2 = db2.cursor()

db = MySQLdb.connect(host="localhost", user="raspi", passwd="warden7", db="clima")
cur = db.cursor()

sensor = W1ThermSensor()

os.system("sudo pkill libgpiod_pulsei")  # Para reiniciar los pulsos del sensor DHT

posiciones10 = [11, 22, 33, 44, 55]
posiciones7 = [11, 20, 30, 40, 50, 60, 70, 80]

camara7 = Camara(7)
camara10 = Camara(10)

camara7.agregarSensor(DHT(1, board.D5))
camara7.agregarSensor(DHT(2, board.D11))
camara7.agregarSensor(DHT(3, board.D9))
camara7.agregarSensor(DHT(4, board.D24))
camara7.agregarSensor(DHT(5, board.D22))
camara7.agregarSensor(DS(6, "3c01f095f809"))
camara7.agregarSensor(DS(7, "3c01f0959343"))
camara7.agregarSensor(DS(8, "3c01f095afbc"))

camara10.agregarSensor(DHT(1, board.D19))
camara10.agregarSensor(DHT(2, board.D13))
camara10.agregarSensor(DHT(3, board.D6))
camara10.agregarSensor(DS(7, "3c01f0959d2d"))
camara10.agregarSensor(DS(7, "3c01f0954842"))

anterior = -1
anthora = -1

while True:

    for i in range(camara7.getTam()):
        camara7.sensores[i].leerdatos()
    for j in range(camara10.getTam()):
        camara10.sensores[j].leerdatos()

    if datetime.datetime.now().minute != anterior:  # Guarda si ha pasado un minuto
        anterior = datetime.datetime.now().minute
        try:
            cur.execute()
            db.commit()
        except:
            pass
        try:
            cur.execute('''TRUNCATE TABLE HUMXTEM;''')
            cur.execute()
            db.commit()
        except:
            pass
        tiempo = datetime.datetime.now()
        try:
            cur2.execute()
            db2.commit()
        except:
            pass
        try:
            cur2.execute())
            db2.commit()
        except:
            pass

    if cur.execute("SELECT * FROM CAMARA7") > (CONST_DATOANIO + CONST_DATOMES):
        cur.execute("DELETE FROM CAMARA7 LIMIT 43200")
    if cur.execute("SELECT * FROM CAMARA10") > (CONST_DATOANIO + CONST_DATOMES):
        cur.execute("DELETE FROM CAMARA10 LIMIT 43200")

    if cur2.execute("SELECT * FROM CAMARA10") > (CONST_DATOSEMANA + CONST_DATODIA):
        cur2.execute("DELETE FROM CAMARA10 LIMIT 1440")
        cur2.execute("DELETE FROM CAMARA7 LIMIT 1440")
    time.sleep(2.0)