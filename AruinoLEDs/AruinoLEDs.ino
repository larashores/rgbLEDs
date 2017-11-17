// Color Changing LEDs

 
const int clockPin = 5;  		//ClockOut to WS2803 pin 4
const int dataPin  = 6;    		//DataOut  to WS2803 pin 5

const int nWS2803s = 1;         //Number of WS2803s being outputted to
const int nRGBs = nWS2803s*6;	//Number of groups of 3 RGB LEDs on WS2803
const int nLEDs = nRGBs*3;		//Number of individual LEds on WS2803

byte ledArray[nLEDs];



void setup() {
    Serial.begin(9600);		//Serial start
    
    //Pin initialization
    pinMode(clockPin, OUTPUT); 
    pinMode(dataPin, OUTPUT);
  
    // Initialize WS2803 - Clock needs to be low at least 600us to prepare itself.
    digitalWrite(clockPin, LOW);
    delayMicroseconds(600);
  
    // Initialize LED arrays - all LEDs OFF.
    

}

void loop() {
	if(Serial.available()){
          loadSerial();
          loadWS2803();
	}
}


void loadSerial(){
    int val;
    int run = 0;
    while(run<nLEDs){
        if(Serial.available()){
            val = Serial.read();
            ledArray[run]=val;
            run++;
        }
    }
}
//------------------WS2803 Interfacing-----------------------------------------
void loadWS2803(){  
    int val;
    for(int led = 0; led < nLEDs; led++){
        val = ledArray[led];
        shiftOut(dataPin, clockPin, MSBFIRST, val-255);
    }
    delayMicroseconds(600); // 600us needed to reset WS2803s
}
