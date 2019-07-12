#include <WiFi.h>
#include <PubSubClient.h>
 
const char* ssid = "RouterPi";
const char* password =  "minhasenha";
const char* mqttServer = "192.168.15.6";
const int mqttPort = 1883;
//const char* mqttUser = "yourMQTTuser";
//const char* mqttPassword = "yourMQTTpassword";
 
WiFiClient espClient;
PubSubClient client(espClient);
int disc = 0;
int con = 0;
int timeout =0;
void setup() {
 
  Serial.begin(115200);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (Serial.println(client.connect("ESP32Client"))) {
 
      Serial.println("connected");
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
 
  client.publish("ArduinoeCia", "Hello from ESP32");
 
}
 
void loop() {
    if( client.connected() ){  
      Serial.print("count ");
      Serial.println(con);
            con++;
    }
     else{
            while (!client.connected()) {
          Serial.println(client.connected());
          Serial.println(WiFi.status());
          if(WiFi.status() != WL_CONNECTED){                           
                      WiFi.begin(ssid, password);
                      timeout = 0;
                      while (WiFi.status() != WL_CONNECTED) {
                        delay(500);
                        Serial.println("Connecting to WiFi..");
                        timeout += 500;
                        if (timeout > 5000) 
                          break;
                      }
                        if (timeout > 5000)
                          break;
                      Serial.println("Connected to the WiFi network");
                      Serial.println("Connecting to MQTT...");
                 
                      if (Serial.println(client.connect("ESP32Client"))) {
                 
                      Serial.println("connected");
                 
                    } else {
                 
                      Serial.print("failed with state ");
                      Serial.print(client.state());
                      delay(2000);
                 
                    }
          }
          Serial.print("discount ");
          Serial.println(disc);
          disc++;
    }
}

if (timeout > 5000){
  Serial.println("Failed to connect WIFI, Timout error");
}
else{
  client.publish("ArduinoeCia","Connected");
  client.publish("ArduinoeCia",String(con).c_str());
  client.publish("ArduinoeCia","Disconnected");
  client.publish("ArduinoeCia",String(disc).c_str());    
}
delay(1000);
}
