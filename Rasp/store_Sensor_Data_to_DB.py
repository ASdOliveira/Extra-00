#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------


import json
import sqlite3
import time

# SQLite DB Name
DB_Name =  "IoT.db"

#===============================================================
# Database Manager Class

class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(DB_Name)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()
        
    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()

#===============================================================
# Functions to push Sensor Data into Database

# Function to save Temperature to DB Table
def DHT22_Temp_Data_Handler(json_Dict, timeStamp):
    #Parse Data 
    #json_Dict = json.loads(jsonData)
    print("3")
    SensorID = str( json_Dict['values'][0]) 
    Data_and_Time = timeStamp
    Temperature = str( json_Dict['values'][1]) 
    #print("already gotten the values")
    
    #Push into DB Table
    dbObj = DatabaseManager()
    #print("dbobj created")
    dbObj.add_del_update_db_record("insert into DHT22_Temperature_Data (SensorID, Date_n_Time, Temperature) values (?,?,?)",[SensorID, Data_and_Time, Temperature])
    del dbObj
    print("Inserted Temperature Data into Database.")
    print("")

# Function to save Humidity to DB Table
def DHT22_Humidity_Data_Handler(json_Dict,timeStamp):
    #Parse Data 
    #json_Dict = json.loads(jsonData)
    print("5")
    SensorID = str( json_Dict['values'][0] )
    Data_and_Time = timeStamp
    Humidity = str( json_Dict['values'][2])
    
    
    #Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into DHT22_Humidity_Data (SensorID, Date_n_Time, Humidity) values (?,?,?)",[SensorID, Data_and_Time, Humidity])
    del dbObj
    print("Inserted Humidity Data into Database.")
    print("")


# Function to save Humidity to DB Table
def FAN_Status_Data_Handler(json_Dict,timeStamp):
    #Parse Data 
    print("6")
    SensorID = str( json_Dict['values'][0] )
    Data_and_Time = timeStamp
    Status = str( json_Dict['values'][3] )
    
    
    #Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into FAN_Status_Data (SensorID, Date_n_Time, Status) values (?,?,?)",[SensorID, Data_and_Time, Status])
    del dbObj
    print("Inserted FAN Status Data into Database.")
    print("")


#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
    
    print("1")
    timeStamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    json_Dict = json.loads(jsonData)
    #print("DeviceId: {}".format(json_Dict["values"][0]))
    #print(type(str(json_Dict["values"][0])))
    print("2")
    DHT22_Temp_Data_Handler(json_Dict,timeStamp)
    print("4")
    DHT22_Humidity_Data_Handler(json_Dict,timeStamp)
    print("6")
    FAN_Status_Data_Handler(json_Dict,timeStamp)
    print("7")
    #json_Dict = json.loads(jsonData)
    #print("DeviceId: {}".format(json_Dict["values"][0]))

#===============================================================
