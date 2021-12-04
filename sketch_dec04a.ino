int redPin = 11;
int greenPin = 9;
int bluePin = 10;
int MoPin = 6; // vibrator Grove connected to digital pin 4
int thres = 100;  //亮度

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
//      未激活状态
//      baseOn(1000,5); 
//      baseOff(1000,5);

//      trigger1状态
//      trigger1On(1000,5);
//      trigger1Off(1000,5);
//      
//      trigger2状态
//      trigger2On(1000,5);
//      trigger2Off(1000,5);
        
//      同时trigger状态        
        bothOn(1000,5);
        bothOff(1000,5);

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

void baseOn(unsigned int time,int increament){
        for (byte value = 0 ; value < thres; value+=increament){ 
            analogWrite(redPin, value);
            analogWrite(greenPin, value*0.4); 
            analogWrite(bluePin, value/4);  
            delay(100);
        } 
}

void baseOff(unsigned int time,int decreament){
        for (byte value = thres; value >0; value-=decreament){ 
            analogWrite(redPin, value);
            analogWrite(greenPin, value*0.4); 
            analogWrite(bluePin, value/4);  
            delay(100); 
        }
}

void trigger1On(unsigned int time,int increament){
        for (byte value = 0 ; value < thres; value+=increament){ 
            analogWrite(redPin, value);
            //analogWrite(greenPin, value*0.4); 
            //analogWrite(bluePin, value/4);  
            delay(100);
        } 
}

void trigger1Off(unsigned int time,int decreament){
        for (byte value = thres; value >0; value-=decreament){ 
            analogWrite(redPin, value);
            //analogWrite(greenPin, value*0.4); 
            //analogWrite(bluePin, value/4);  
            delay(100); 
        }
}

void trigger2On(unsigned int time,int increament){
        for (byte value = 0 ; value < thres; value+=increament){ 
            //analogWrite(redPin, value);
            //analogWrite(greenPin, value*0.4); 
            analogWrite(bluePin, value);  
            delay(100);
        } 
}

void trigger2Off(unsigned int time,int decreament){
        for (byte value = thres; value >0; value-=decreament){ 
//            analogWrite(redPin, value);
//            analogWrite(greenPin, value*0.4); 
            analogWrite(bluePin, value);  
            delay(100); 
        }
}

void bothOn(unsigned int time,int increament){
        for (byte value = 0 ; value < thres; value+=increament){ 
            analogWrite(redPin, value);
            delay(100);
            //analogWrite(greenPin, value*0.4); 
            analogWrite(bluePin, value);  
            delay(100);
        } 
}

void bothOff(unsigned int time,int decreament){
        for (byte value = thres; value >0; value-=decreament){ 
            analogWrite(redPin, value);
            delay(100);
            //analogWrite(greenPin, value*0.4); 
            analogWrite(bluePin, value);  
            delay(100); 
        }
}

//void fadeOn(unsigned int time,int increament){
//        for (byte value = 0 ; value < 255; value+=increament){ 
//            analogWrite(redPin, constrain(value,0,255));
//            analogWrite(greenPin, constrain(value,0,255)); 
//            analogWrite(bluePin, constrain(value,0,255));  
//            delay(100);
//        } 
//}
//
//void fadeOff(unsigned int time,int decreament){
//        for (byte value = 255; value >0; value-=decreament){ 
//            analogWrite(redPin, constrain(value,0,255));
//            analogWrite(greenPin, constrain(value,0,255)); 
//            analogWrite(bluePin, constrain(value,0,255));  
//                delay(time/(255/5)); 
//        }
//}
