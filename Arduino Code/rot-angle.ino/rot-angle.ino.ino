
#define ROT_ANGLE A1

String checkcom = "ANGLE_CHECK";
String com1 = "ANGLE_90";
String com2 = "ANGLE_180";
String com3 = "ANGLE_T";
int value;
//int mapped_value;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ROT_ANGLE, INPUT);
}

float get_angle(int pin){
  int adc_ref = 5;      //reference voltage of ADC is 5V.If the VCC switch on the Uno board switches to 3V3, the ADC_REF should be 3.3
  int vcc = 5;          //VCC of the grove interface is normally 5V
  int full_angle = 360; //full value of the rotary angle is 300 degrees
  
  int sensor_value = analogRead(pin);
  float voltage = (float)sensor_value*adc_ref/1023;
  float degrees_rotated = (voltage*full_angle)/vcc;
  return degrees_rotated;
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    String var = Serial.readStringUntil("/r");
    if(var == checkcom){
      value = get_angle(ROT_ANGLE);
      Serial.println(value);
      //mapped_value = map(value, 0, 800, 0, 10);
      //Serial.println(mapped_value);
    }
    else if(var == com1) {
      Serial.println(com1);
    }
    else if(var == com2) {
      Serial.println(com2);
    }
    else if(var == com3) {
      delay(3000);
      Serial.println(com3);
    }
  }
}
