#include <Arduino.h>
#include <SoftwareSerial.h>
#include <DHT22.h>
#include <OneWire.h>

void wait(){
    while(true){
        if(Serial.readString()!="")
            break;
        delay(500);
    }
}

// pH Sensor 
SoftwareSerial phSerial(4,5);

String getpH(){
    bool phComplete = false;
    String pH;
    while(phSerial.available())
        phSerial.read();
    delay(1000);
    while(phSerial.available() &&!phComplete) {                     
    	char inchar = (char)phSerial.read();             
    	pH += inchar;
    	if (inchar == '\r') {
      	    phComplete = true;                  
        }
    }
    return pH;
}

// DHT 22
DHT22 dht(2);

// TMP 
OneWire tmp(3);
bool found = false;
byte addr[8];

float getWaterTemp(){
    int i;
    byte rdata[12];
    if(!found){
        if (!tmp.search(addr)){
            tmp.reset_search();
            return 0;
        }
        else
            found = true;
    }
  
    tmp.reset();
    tmp.select(addr);
    tmp.write(0x44, 1); 
  
    delay(1000); 

    tmp.reset();
    tmp.select(addr);    
    tmp.write(0xBE); 
    for ( i = 0; i < 9; i++) rdata[i] = tmp.read();
    int16_t raw = (rdata[1] << 8) | rdata[0];
    return ((float)raw / 16.0) * 1.8 + 32.0;
}

// Pin Initialization
void setup(){
    Serial.begin(9600);
    phSerial.begin(9600); 
}

// Data RX/TX
void loop(){

    // Wait for go ahead    
    // wait();
    
    dht.readData();

    // Format Data
    String data;
    
    data =  "RTmp:";
    data += String(dht.getTemperatureF()) + "\n"; 
    
    data += "Humi:";
    data += String(dht.getHumidity()) + "\n";

    data += "WTmp:";
    data += String(getWaterTemp()) + "\n";

    data += "WLvl:";
    data += String(analogRead(A0)) + "\n";

    data += "Lite:";
    data += String(analogRead(A1)) + "\n";
     
    data += "pH:";
    data += getpH() + "\n";

    // Send data Serially
    if (Serial)
        Serial.println(data);
    
    delay(1000);
}
