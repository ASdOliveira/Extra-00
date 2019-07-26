from dbfunctions import *

con = Conexao('localhost','postgres','postgres','00265ad2b6e1')
temp = 36.9
id = 1
sql = 'INSERT INTO "DHT22_Temperature_Data" ("Temperature", "Date_n_Time", "SensorID") VALUES (%s,current_timestamp,%s);'
param = [temp,id]
#sql = "INSERT INTO cidade values (default, 'Rio de Janeiro', 'SP')"
rs=con.consultar('SELECT * FROM "DHT22_Temperature_Data";')
print(rs)
con.fechar()
