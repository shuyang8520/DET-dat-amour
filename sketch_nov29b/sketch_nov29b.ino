//项目五 – 炫彩RGB灯
int redPin = 9;
int greenPin = 10;
int bluePin = 11;
int MoPin = 6; // vibrator Grove connected to digital pin 4

void setup() {
  // put your setup code here, to run once:
     pinMode(redPin, OUTPUT);
     pinMode(greenPin, OUTPUT);
     pinMode(bluePin, OUTPUT);
     //确定点位
     pinMode( MoPin, OUTPUT );
}

void loop() {
  // put your main code here, to run repeatedly:
      //R:0-255 G:0-255 B:0-255
      //colorRGB(random(0,255),random(0,255),random(0,255));  
  //delay(1000);
      fadeOn(1000,5);
      fadeOff(1000,5);

//      digitalWrite(MoPin, HIGH);
//      delay(1000);
//      digitalWrite(MoPin, LOW);
//      delay(1000); 
}
//void colorRGB(int red, int green, int blue){
//            analogWrite(redPin,constrain(red,0,255));
//            analogWrite(greenPin,constrain(green,0,255));
//analogWrite(bluePin,constrain(blue,0,255));
//}
void fadeOn(unsigned int time,int increament){
        for (byte value = 0 ; value < 255; value+=increament){ 
            analogWrite(redPin, constrain(value,0,255));
            analogWrite(greenPin, constrain(value,0,255)); 
            analogWrite(bluePin, constrain(value,0,255));  
            delay(time/(255/5));
        } 
}

void fadeOff(unsigned int time,int decreament){
        for (byte value = 255; value >0; value-=decreament){ 
            analogWrite(redPin, constrain(value,0,255));
            analogWrite(greenPin, constrain(value,0,255)); 
            analogWrite(bluePin, constrain(value,0,255));  
                delay(time/(255/5)); 
        }
}
