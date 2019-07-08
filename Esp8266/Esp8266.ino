/*
 * Projeto destinado à monitorar a temperatura de um ambiente utilizando MQTT
 * 
 * O Broker envia uma solicitação ao ESP8266 que devolve a temperatura. 
 * O tópico no qual ele vai escrever é o nome do device.
 * 
 * Arysson Oliveira
*/
#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
#include "DHT.h"


// DHT 
#define DHTPIN 5
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

long lastTime;


//WiFi
const char* SSID = "casa";           // SSID da rede WiFi que deseja se conectar
const char* PASSWORD = "garantia";   // Senha da rede WiFi que deseja se conectar
WiFiClient wifiClient;                        

/*
//MQTT Server Online
const char* BROKER_MQTT = "m15.cloudmqtt.com"; //URL do broker MQTT que se deseja utilizar
int BROKER_PORT = 11597;                      // Porta do Broker MQTT
const char* user = "petateba";
const char* pass = "PFVknub1lGVQ";
*/

//MQTT Server Raspberry Settings
const char* BROKER_MQTT = "192.168.0.103"; //URL do broker MQTT que se deseja utilizar
int BROKER_PORT = 1883;                      // Porta do Broker MQTT
const char* user = "pi";
const char* pass = "pi";

//ID and Topic to publish
#define ID_MQTT  "Device 1"            
#define TOPIC_PUBLISH "Temp"        //Informe um Tópico único. Caso sejam usados tópicos em duplicidade, o último irá eliminar o anterior.
#define TOPIC_SUBSCRIBE "Temp Rx"

PubSubClient MQTT(wifiClient);        // Instancia o Cliente MQTT passando o objeto espClient

//Declaração das Funções
void mantemConexoes();  //Garante que as conexoes com WiFi e MQTT Broker se mantenham ativas
void conectaWiFi();     //Faz conexão com WiFi
void conectaMQTT();     //Faz conexão com Broker MQTT
void enviaPacote();     //
void recebePacote(char* topic, byte* payload, unsigned int length);      

  
void setup() 
{
  Serial.begin(115200);
  dht.begin();
  conectaWiFi();
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
  MQTT.setCallback(recebePacote); 
}

void loop() 
{
  mantemConexoes();
  //enviaPacote();
  MQTT.loop();
}

void mantemConexoes() 
{
  if (!MQTT.connected()) 
  {
     conectaMQTT(); 
  }
  
  conectaWiFi(); //se não há conexão com o WiFI, a conexão é refeita
}

void conectaWiFi() {

  if (WiFi.status() == WL_CONNECTED) 
  {
     return;
  }
        
  Serial.print("Conectando-se na rede: ");
  Serial.print(SSID);
  Serial.println("  Aguarde!");

  WiFi.begin(SSID, PASSWORD); // Conecta na rede WI-FI  
  
  while (WiFi.status() != WL_CONNECTED) 
  {
      delay(100);
      Serial.print(".");
  }
  
  Serial.println();
  Serial.print("Conectado com sucesso, na rede: ");
  Serial.print(SSID);  
  Serial.print("  IP obtido: ");
  Serial.println(WiFi.localIP()); 
}

void conectaMQTT() 
{ 
  while (!MQTT.connected()) 
  {
      Serial.print("Conectando ao Broker MQTT: ");
      Serial.println(BROKER_MQTT);
      if (MQTT.connect(ID_MQTT,user,pass)) 
      {
        MQTT.subscribe(TOPIC_SUBSCRIBE);
        Serial.println("Conectado ao Broker com sucesso!");
      } 
      else 
      {
          Serial.println("Nao foi possivel se conectar ao broker.");
          Serial.println("Nova tentatica de conexao em 5s");
          delay(5000);
      }
  }
}

void recebePacote(char* topic, byte* payload, unsigned int length)
{
  String msg;
  for(int i=0;i<length;i++)
  {
    char c = (char)payload[i];
    msg += c;
  }

 Serial.print("Mensagem recebida: ");
 Serial.println(msg);
 Serial.print("Topic:  ");
 Serial.println(topic);
  if(msg == "1")
  {
    enviaPacote();
  }
   
}

void enviaPacote() 
{
  
  //if( (millis() - lastTime) > 3000)
  //{
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    //hora = hora + 1;
    //Serial.println(t);
    Serial.println(String(t).c_str());
    MQTT.publish(TOPIC_PUBLISH, String(t).c_str());
    //MQTT.publish(TOPIC_PUBLISH2, String(h).c_str());
    //MQTT.publish(TOPIC_PUBLISH3, String(hora).c_str());
    //lastTime = millis();
  //}
         
}