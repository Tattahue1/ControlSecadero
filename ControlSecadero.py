from requests import get
import datetime
import pandas as pd
import os, signal
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

os.system("sudo pkill libgpiod_pulsei") #Para reiniciar los pulsos del sensor DHT

dhtDevice5 = adafruit_dht.DHT22(board.D22,use_pulseio = True) #Camara 7
dhtDevice4 = adafruit_dht.DHT22(board.D10,use_pulseio = True)
dhtDevice3 = adafruit_dht.DHT22(board.D9,use_pulseio = True)
dhtDevice2 = adafruit_dht.DHT22(board.D11,use_pulseio = True)
dhtDevice1 = adafruit_dht.DHT22(board.D5,use_pulseio = True) #6, 13, 19

dhtDevicecam1 = adafruit_dht.DHT22(board.D19,use_pulseio = True) #Camara 10
dhtDevicecam2 = adafruit_dht.DHT22(board.D13,use_pulseio = True)
dhtDevicecam3 = adafruit_dht.DHT22(board.D6,use_pulseio = True)

temperature_c1 =0
humidity1 =0
temperature_c2 =0
humidity2 =0
temperature_c3 =0
humidity3 =0
temperature_c4 =0
humidity4 =0
temperature_c5 =0
humidity5 =0
tempsensor6 = 0
tempsensor7 = 0
tempsensor8 = 0


temperaturec1 =0
humidityc1 =0
temperaturec2 =0
humidityc2 =0
temperaturec3 =0
humidityc3 =0

tempsensorc4 = 0
tempsensorc5 = 0

anterior = -1
anthora = -1

#Obtencion de datos de cada sensor
while True:
   
    #     Codigo que guarda los datos del sensor en archivos .csv
    if datetime.datetime.now().minute != anterior: #Guarda si ha pasado un minuto
        anterior = datetime.datetime.now().minute
        ahora=datetime.datetime.now()
        ahora = str(ahora)[0:10]
        file = "/home/pi/Pruebas/" +ahora + "camara7" + ".csv"
        try:
            df=pd.read_csv(file)
            df=df.drop('Unnamed: 0',axis=1)
            aux= datetime.datetime.now()
            aux = str(aux)[11:16]
            df=df.append({'Hora':aux,'Temp 1':temperature_c1,'Temp 2':temperature_c2,
                          'Temp 3':temperature_c3,'Temp 4':temperature_c4,'Temp 5':temperature_c5,
                          'Humedad 1':humidity1,'Humedad 2':humidity2,'Humedad 3':humidity3,
                          'Humedad 4':humidity4,'Humedad 5':humidity5,'Sensor 6':tempsensor6,
                          'Sensor 7':tempsensor7,'Sensor 8':tempsensor8},ignore_index=True)
            file = "/home/pi/Pruebas/" +ahora+ "camara7" + ".csv"
            df.to_csv(file)
        except:
            aux= datetime.datetime.now()
            aux = str(aux)[11:16]
            df=pd.DataFrame(columns = ['Hora', 'Temp 1','Humedad 1','Temp 2','Humedad 2','Temp 3',
                                      'Humedad 3','Temp 4','Humedad 4','Temp 5','Humedad 5',
                                      'Sensor 6', 'Sensor 7','Sensor 8'])
            df=df.append({'Hora':aux,'Temp 1':temperature_c1,'Temp 2':temperature_c2,
                          'Temp 3':temperature_c3,'Temp 4':temperature_c4,'Temp 5':temperature_c5,
                          'Humedad 1':humidity1,'Humedad 2':humidity2,'Humedad 3':humidity3,
                          'Humedad 4':humidity4,'Humedad 5':humidity5,'Sensor 6':tempsensor6,
                          'Sensor 7':tempsensor7,'Sensor 8':tempsensor8},ignore_index=True)
            file = "/home/pi/Pruebas/" +ahora + "camara7"+ ".csv"
            df.to_csv(file)
           
        file2 = "/home/pi/Pruebas/" +ahora + "camara10" + ".csv"  
        try:
            df=pd.read_csv(file2)
            df=df.drop('Unnamed: 0',axis=1)
            aux= datetime.datetime.now()
            aux = str(aux)[11:16]
            print(aux)
            df=df.append({'Hora':aux,'Temp 1':tempsensorc1,'Temp 2':tempsensorc2,
                          'Temp 3':tempsensorc3,'Temp 4':tempsensorc4,'Temp 5':tempsensorc5,
                          'Humedad 1':humidityc1,'Humedad 2':humidityc2,'Humedad 3':humidityc3},ignore_index=True)
            file2 = "/home/pi/Pruebas/" +ahora+ "camara10" + ".csv"
            df.to_csv(file2)
        except:
            aux= datetime.datetime.now()
            aux = str(aux)[11:16]
            df=pd.DataFrame(columns = ['Hora', 'Temp 1','Humedad 1','Temp 2','Humedad 2','Temp 3',
                                      'Humedad 3','Temp 4','Temp 5'])
            df=df.append({'Hora':aux,'Temp 1':temperaturec1,'Temp 2':temperaturec1,
                          'Temp 3':temperaturec1,'Temp 4':temperaturec1,'Temp 5':temperaturec1,
                          'Humedad 1':humidityc1,'Humedad 2':humidityc2,'Humedad 3':humidityc3},ignore_index=True)
            file2 = "/home/pi/Pruebas/" +ahora + "camara10"+ ".csv"
            df.to_csv(file2)
       
    if datetime.datetime.now().hour != anthora: #Guarda si ha pasado una hora
        anthora = datetime.datetime.now().hour
        ahora=datetime.datetime.now()
        ahora = str(ahora)[0:10]
        file = "/home/pi/Pruebas/" + ahora + "HORAS"+ "camara7" + ".csv"
        try:
            df=pd.read_csv(file)
            df=df.drop('Unnamed: 0',axis=1)
            df=df.append({'Hora':datetime.datetime.now().hour,'Temp 1':temperature_c1,'Temp 2':temperature_c2,
                          'Temp 3':temperature_c3,'Temp 4':temperature_c4,'Temp 5':temperature_c5,
                          'Humedad 1':humidity1,'Humedad 2':humidity2,'Humedad 3':humidity3,
                          'Humedad 4':humidity4,'Humedad 5':humidity5,'Sensor 6':tempsensor6,
                          'Sensor 7':tempsensor7,'Sensor 8':tempsensor8},ignore_index=True)
            file = "/home/pi/Pruebas/" +ahora + "HORAS"+ "camara7" + ".csv"
            df.to_csv(file)
        except:
            df=pd.DataFrame(columns = ['Hora', 'Temp 1','Humedad 1','Temp 2','Humedad 2','Temp 3',
                                      'Humedad 3','Temp 4','Humedad 4','Temp 5','Humedad 5',
                                      'Sensor 6', 'Sensor 7','Sensor 8'])
            df=df.append({'Hora':datetime.datetime.now().hour,'Temp 1':temperature_c1,'Temp 2':temperature_c2,
                          'Temp 3':temperature_c3,'Temp 4':temperature_c4,'Temp 5':temperature_c5,
                          'Humedad 1':humidity1,'Humedad 2':humidity2,'Humedad 3':humidity3,
                          'Humedad 4':humidity4,'Humedad 5':humidity5,'Sensor 6':tempsensor6,
                          'Sensor 7':tempsensor7,'Sensor 8':tempsensor8},ignore_index=True)
            file ="/home/pi/Pruebas/" + ahora + "HORAS"+ "camara7" + ".csv"
            df.to_csv(file)
       
        file2 = "/home/pi/Pruebas/" + ahora + "HORAS"+ "camara10" + ".csv"
        try:
            df=pd.read_csv(file2)
            df=df.drop('Unnamed: 0',axis=1)
            df=df.append({'Hora':datetime.datetime.now().hour,'Temp 1':tempsensorc1,'Temp 2':tempsensorc2,
                          'Temp 3':tempsensorc3,'Temp 4':tempsensorc4,'Temp 5':tempsensorc5,
                          'Humedad 1':humidityc1,'Humedad 2':humidityc2,'Humedad 3':humidityc3},ignore_index=True)
            file2 = "/home/pi/Pruebas/" +ahora + "HORAS"+ "camara10" + ".csv"
            df.to_csv(file2)
        except:
            df=pd.DataFrame(columns = ['Hora', 'Temp 1','Humedad 1','Temp 2','Humedad 2','Temp 3',
                                      'Humedad 3','Temp 4','Temp 5'])
            df=df.append({'Hora':datetime.datetime.now().hour,'Temp 1':temperaturec1,'Temp 2':temperaturec1,
                          'Temp 3':temperaturec1,'Temp 4':temperaturec1,'Temp 5':temperaturec1,
                          'Humedad 1':humidityc1,'Humedad 2':humidityc2,'Humedad 3':humidityc3},ignore_index=True)
            file2 ="/home/pi/Pruebas/" + ahora + "HORAS"+ "camara10" + ".csv"
            df.to_csv(file2)
           
   
    #Obtencion de datos de cada sensor
    try:
        temperature_c1 = dhtDevice1.temperature
        humidity1 = dhtDevice1.humidity
    except RuntimeError as error:
        continue
    except Exception as error:
        pass
   
    try:
        temperature_c2 = dhtDevice2.temperature
        humidity2 = dhtDevice2.humidity
    except RuntimeError as error:
        continue
    except Exception as error:
        pass
   
    try:
        temperature_c3 = dhtDevice3.temperature
        humidity3 = dhtDevice3.humidity
    except RuntimeError as error:
        continue
    except Exception as error:
        pass
   
    try:
        temperature_c4 = dhtDevice4.temperature
        humidity4 = dhtDevice4.humidity
    except RuntimeError as error:
        continue
    except Exception as error:
        pass  
   
    try:
        temperature_c5 = dhtDevice5.temperature
        humidity5 = dhtDevice5.humidity
    except RuntimeError as error:
        continue
    except Exception as error:
        pass
   
    try:
        temperaturec1 = dhtDevicecam1.temperature
        humidityc1 = dhtDevicecam1.humidity
    except RuntimeError as error:
        continue
    except Exception as error:
        pass
   
    try:
        temperaturec2 = dhtDevicecam2.temperature
        humidityc2 = dhtDevicecam2.humidity
    except RuntimeError as error:
        continue
    except Exception as error:
        pass
   
    try:
        temperaturec3 = dhtDevicecam3.temperature
        humidityc3 = dhtDevicecam3.humidity
    except RuntimeError as error:
        continue
    except Exception as error:
        pass
   
    try:
        for sensor in W1ThermSensor.get_available_sensors():
            if sensor.id == "3c01f095afbc": #sensor 8
                tempsensor8 = sensor.get_temperature()
            elif sensor.id == "3c01f0959343": #sensor 7
                tempsensor7 = sensor.get_temperature()
            elif sensor.id == "3c01f095f809": #sensor 6
                tempsensor6 = sensor.get_temperature()
            elif sensor.id == "3c01f0959d2d": #sensor 6
                temperaturec4 = sensor.get_temperature()
            else:
                temperaturec5 = sensor.get_temperature()
#             Sen 6 = 809  Sen 7 = 343 Sen 8 = fbc
    except Exception as error:
        pass
   
    time.sleep(2.0)
        raise error
    time.sleep(2.0)
