// Blind-Band Project code
// Project can be accessed at https://www.instructables.com/Blind-Band/


//Define variables
const int EchoPin1 = 2;
const int TriggerPin1 = 3;

const int EchoPin2 = 4;
const int TriggerPin2 = 5;

const int EchoPin3 = 6;
const int TriggerPin3 = 7;

const int EchoPin4 = 8;
const int TriggerPin4 = 9;

int vibrator1 = A0;
int vibrator2 = A1;
int vibrator3 = A2;
int vibrator4 = A3;
int vibrator5 = A4;
int vibrator6 = A5;

int cm1, cm2, cm3, cm4;

void setup() { //initialize components

  Serial.begin(9600);
  pinMode(TriggerPin1, OUTPUT);
  pinMode(EchoPin1, INPUT);

  pinMode(TriggerPin2, OUTPUT);
  pinMode(EchoPin2, INPUT);

  pinMode(TriggerPin3, OUTPUT);
  pinMode(EchoPin3, INPUT);

  pinMode(TriggerPin4, OUTPUT);
  pinMode(EchoPin4, INPUT);

  pinMode(vibrator1, OUTPUT);
  pinMode(vibrator2, OUTPUT);
  pinMode(vibrator3, OUTPUT);
  pinMode(vibrator4, OUTPUT);
  pinMode(vibrator5, OUTPUT);
  pinMode(vibrator6, OUTPUT);

}

void loop()
{
  cm1 = ping(3, 2); //left 
  cm2 = ping(5, 4); //front 
  cm3 = ping(7, 6); //right 
  cm4 = ping(9,8); //back

/*Setting: 1. Activation ranges and micro-vibrators pins according to distance and origin of the object. 2. Intensity of the motors according to the distance between the object (it can be hard or soft)*/
  if (cm1 > 40 && cm1 < 80) {
    SoftVibration (vibrator1);
    SoftVibration (vibrator2);
  }

else if (cm1 > 10 && cm1 <= 40) {
  HardVibration (vibrator1); 
  HardVibration (vibrator2); 
  }

if (cm2 > 40 && cm2 < 80) {
  SoftVibration (vibrator3);
  SoftVibration (vibrator4);
  }

else if (cm2 > 10 && cm2 <= 40) {
  HardVibration (vibrator3);
  HardVibration (vibrator4);
  }

if (cm3 > 40 && cm3 < 80) {
  SoftVibration (vibrator5); 
  SoftVibration (vibrator6);
  }

else if (cm3 > 10 && cm3 <= 40) {
  HardVibration (vibrator5);
  HardVibration (vibrator6);
  }

if (cm4 > 40 && cm4 < 80) {
  SoftVibration (vibrator6);
  SoftVibration (vibrator1);
  }

else if (cm4 > 10 && cm4 <= 40) { 
    HardVibration (vibrator6); 
    HardVibration (vibrator1); 
}

// Front-Left Diagonal 
if (cm1 > 40 && cm2 > 40 && cm1 < 80 && cm2 < 80) { 
    SoftVibration (vibrator2); 
    SoftVibration (vibrator3); 
}

if (cm1 > 10 && cm2 > 10 && cm1 <= 40 && cm2 <= 40) { 
    HardVibration (vibrator2); 
    HardVibration (vibrator3); 
}

// Front-Right Diagonal 
if (cm2 > 40 && cm3 > 40 && cm2 < 80 && cm3 < 80) { 
    SoftVibration (vibrator4); 
    SoftVibration (vibrator5); 
}

if (cm2 > 10 && cm3 > 10 && cm2 <= 40 && cm3 <= 40) { 
    HardVibration (vibrator4); 
    HardVibration (vibrator5); 
}

// Back-Right Diagonal 
if (cm3 > 40 && cm4 > 40 && cm3 < 80 && cm4 < 80) { 
    SoftVibration (vibrator6); 
}

if (cm3 > 10 && cm4 > 10 && cm3 <= 40 && cm4 <= 40) { 
    HardVibration (vibrator6); 
}

// Back-Left Diagonal 
if (cm1 > 40 && cm4 > 40 && cm1 < 80 && cm4 < 80) { 
    SoftVibration (vibrator1); 
}

if (cm1 > 10 && cm4 > 10 && cm1 <= 40 && cm4 <= 40) { 
    HardVibration (vibrator1); 
}

Serial.print("Distancia: "); 
Serial.println(cm1); 
Serial.println(cm2); 
Serial.println(cm3); 
delay(1000); 
}

void SoftVibration (int pin) { 
    // Set intensity of soft vibration 
    analogWrite (pin, 150); 
    delay(100); 
    analogWrite (pin, 0); 
    delay(100); 
}

void HardVibration (int pin) { 
    // Set intensity of hard vibration 
    analogWrite (pin, 250); 
    delay(100); 
    analogWrite (pin, 0); 
    delay(100); 
}

int ping(int TriggerPin, int EchoPin) { 
    // Ultrasonic sensor function 
    long duration, distanceCm;

    digitalWrite(TriggerPin, LOW); 
    // to generate a clean trigger, we put it in LOW for 4us (microseconds) 
    delayMicroseconds(4); 
    digitalWrite(TriggerPin, HIGH); 
    // generate the Trigger of 10us (microseconds) 
    delayMicroseconds(10); 
    digitalWrite(TriggerPin, LOW);

    duration = pulseIn(EchoPin, HIGH); 
    // measure the time between pulses, in microseconds

    distanceCm = ((duration * (10.0 / 292.0)) / 2); 
    // convert the distance to cm

    return distanceCm; 
}
