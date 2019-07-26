import json
from dbfunctions import *

#===============================================================
# Auxiliar Functions
def boolToInt(bul):
    if bul:
        return 1
    return 0

# Function to save Temperature to DB Table
def DHT22_Temp_Data_Handler(json_Dict):
    #Parse Data 
    
    #print("3")    
    SensorID = json_Dict['values'][0]
    Temperature = json_Dict['values'][1] 
    #print("4")
    #Push intoDB Table
    con = Conexao('localhost','postgres','postgres','00265ad2b6e1')
    sql = 'INSERT INTO "DHT22_Temperature_Data" ("Temperature","Date_n_Time", "SensorID") VALUES (%s,current_timestamp,%s);'
    param = [Temperature,SensorID]
    if con.manipular(sql,param):
        print("Inserted Temperature Data into Database.")
    else:
        print("Error when tried to insert Temperature into Database.")

# Function to save Humidity to DB Table
def DHT22_Humidity_Data_Handler(json_Dict):
    #Parse Data 
    #json_Dict = json.loads(jsonData)
    #print("5")
    SensorID = json_Dict['values'][0]
    Humidity = json_Dict['values'][2]
    #Push into DB Table
    con = Conexao('localhost','postgres','postgres','00265ad2b6e1')
    sql = 'INSERT INTO "DHT22_Humidity_Data" ("Humidity", "Date_n_Time", "SensorID") VALUES (%s,current_timestamp,%s);'
    param = [Humidity,SensorID]
    if con.manipular(sql,param):
        print("Inserted Humidity Data into Database.")
    else:
        print("Error when tried to insert Humidity into Database.")


# Function to save Humidity to DB Table
def FAN_Status_Data_Handler(json_Dict):
    #Parse Data 
    
    SensorID = json_Dict['values'][0]
    Status = json_Dict['values'][3]
    
    
    #Push into DB Table
    con = Conexao('localhost','postgres','postgres','00265ad2b6e1')
    sql = 'INSERT INTO "FAN_Status_Data" ("Status", "Date_n_Time", "SensorID") VALUES  (%s,current_timestamp,%s);'
    param = [boolToInt(Status),SensorID]
    if con.manipular(sql,param):
        print("Inserted FAN Status Data into Database.")
    else:
        print("Error when tried to insert Fan Status into Database.")


#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
    #print("1")
    json_Dict = json.loads(jsonData)  
    #print("2")    
    DHT22_Temp_Data_Handler(json_Dict)
    #print("3")
    DHT22_Humidity_Data_Handler(json_Dict)
   
    FAN_Status_Data_Handler(json_Dict)
    print("DeviceId: {}".format(json_Dict["values"][0]))

#===============================================================
