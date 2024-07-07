#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <ESPAsyncWebServer.h>
#include <StringArray.h>
#include <WiFi.h>

#define echo 13
#define trig 12
#define Button_USC 17
#define LED 15
#define LED2 5


Adafruit_MPU6050 mpu;

long  duration;
float Angle=32;
long int distance=32;
boolean flag_State= false;

const char* ssid = "Esp32";
const char* password = "12345678";
AsyncWebServer server(80);

int flagClicked=0;

int getDistance(){
  Serial.println("generating wave");
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;
  Serial.print("Distance: ");
  Serial.println(distance);
  return distance;
}


void initMPU() {
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  Serial.println("MPU6050 Found!");
}

float getAccReadings() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float Y = atan2(-a.acceleration.x, sqrt(pow(a.acceleration.y, 2) )) * 180 / M_PI ;

  return Y;
}


void setup() {
  initMPU();

  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);
  pinMode(LED,OUTPUT);
    pinMode(LED2,OUTPUT);


  pinMode(Button_USC,INPUT);
  Serial.begin(115200);
  digitalWrite(LED,LOW);
  WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
  server.on("/data", HTTP_GET, [](AsyncWebServerRequest* request) {
    request->send(200, "text/plain", String(Angle));
    flag_State=false;
  });
  
  server.on("/status_tell", HTTP_GET, [](AsyncWebServerRequest* request) {
    // Assuming imageAvailable is a boolean indicating whether an image is available
    request->send_P(200, "text/plain", flag_State ? PSTR("2") : PSTR("3"));
    
  });
    server.begin();
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());


  

    
}

void loop() {



  digitalWrite(LED, LOW);
  float FirstReading = 0;
  float LastReading = 0;

  if (digitalRead(Button_USC) == LOW) {
    digitalWrite(LED2,HIGH);
    int distance=  getDistance();      

    FirstReading = getAccReadings();

    while (digitalRead(Button_USC) == LOW) {
  }
    flagClicked=1;
    digitalWrite(LED2,LOW);
  }
  if (flagClicked==1){
    LastReading = getAccReadings();

    Angle=(LastReading - FirstReading);
    
    flagClicked=0;
    digitalWrite(LED, HIGH);
    flag_State=true;
delay(5000);
}
 delay(100); 
}
