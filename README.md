# rube-goldberg

# Explanation of main.ino
## Setting up libraries and pins
>In this section, we import `pitches.h` which includes the notes for the song as well as the `analogWave` library which allows us to use the UNO R4 DAC.

>The `BUZZER_PIN` is for the PWM tone generation

>We also define pins for both motors and the proximity sensor
```c
#include "pitches.h"
#include "analogWave.h" // Include the library for analog waveform generation

//PINS
#define BUZZER_PIN 5
//Motor 1
#define DIRECTION1 12
#define MOTOR1 3
#define BRAKE1 9

//Motor 2
#define DIRECTION2 13
#define MOTOR2 11
#define BRAKE2 8
//Sensors
#define SENSE1 10


//music stuff
analogWave wave(DAC);   // Create an instance of the analogWave class, using the DAC pin
```
## Variables
```cpp
int b1Duration = 0;  //first tone duration variable
int b2Duration = 0; //second tone duration variable
int cycle1 = 0;     //first tone note counter
int cycle2 = 0;    //second tone note counter
int length = 750;  //tone limit before looping
int reset = 0;     //placeholder to reset counter
int step = 0;      //step of actuator sequence
int confidence = 0; //increases with proximity sensor duration
```

## Setup Function
>Set pinmodes, setup serial, setup DAC
```cpp
void setup() {
  Serial.begin(9600);
  //Setup DAC
  wave.square(10);
  wave.stop();
  //Set up pinmodes
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(DIRECTION1, OUTPUT);
  pinMode(MOTOR1, OUTPUT);
  pinMode(BRAKE1, OUTPUT);
  pinMode(DIRECTION2, OUTPUT);
  pinMode(MOTOR2, OUTPUT);
  pinMode(BRAKE2, OUTPUT);

  pinMode(A3, INPUT);

  pinMode(SENSE1, INPUT);
  pinMode(A1, INPUT);
}
```

## Song Functions
### Play/Stop Functions
> Functions to control the two modes of tone generation
```cpp

void play1(int freq) {
  wave.freq(freq);
}

void stop1() {
  wave.stop();
}

void play2(int freq) {
  tone(BUZZER_PIN, freq);
}

void stop2() {
  noTone(BUZZER_PIN);
}
```
### newMillis
> Normalizes millis value after loop exceeds `length` variable
```cpp
int newMillis() {
  return millis() - reset;
}
```
### music
> When run, checks tone sequences from `pitches.h` and figures out which actions to take based on current time
```cpp
void music() {
if(newMillis() <= 31000) {
  if (newMillis() >= b1Duration && cycle1 < length) {
    // play current note
    if (toneSequence1[cycle1][1] > 0) {
      play1(toneSequence1[cycle1][1]);
    }
    else {
      // if the value of the note is -1, play no sound (rest)
      stop1();
    }
    
    // set next note duration
    b1Duration = newMillis() + toneSequence1[cycle1][0];
    cycle1++;
  }
  

  if (newMillis() >= b2Duration && cycle2 < length) {
    // play current note
    if (toneSequence2[cycle2][1] > 0) {
      play2(toneSequence2[cycle2][1]);
    }
    else {
      // if the value of the note is -1, play no sound (rest)
      stop2();
    }
    
    // set next note duration
    b2Duration = newMillis() + toneSequence2[cycle2][0];
    cycle2++;
  }}
  else {
  reset = millis();
  cycle1 = 0;
  cycle2 = 0;
  b1Duration = 0;
  b2Duration = 0;
  stop1();
  stop2();
  }
}
```
## Actuator Functions
### pushPencil
> Pulses `MOTOR1` (linear actuator) to push pencil into sharpener by reversing direction rapidly
```cpp
void pushPencil() {
  digitalWrite(DIRECTION1, HIGH);
  digitalWrite(BRAKE1, LOW);
  analogWrite(MOTOR1, 255);
  int count = 100;
  bool direction = false;
  while(count > 0) {
    if(direction){
      digitalWrite(DIRECTION1, HIGH);
      delay(100);
    }
    else {
      digitalWrite(DIRECTION1, LOW);
    }
    delay(50);
    direction = !direction;
    count--;
    
  }
  delay(1000);
  analogWrite(MOTOR1, 0);
}
```
### moveUpSlider
> Uses `MOTOR2` to bring `MOTOR1` into position
```cpp
void moveUpSlider() {
  digitalWrite(DIRECTION2, LOW);
  digitalWrite(BRAKE2, LOW);
  analogWrite(MOTOR2, 100);
  delay(500);
  analogWrite(MOTOR2, 90);
}
```
### moveDownSlider
> Uses `MOTOR2` to lower `MOTOR1`
```cpp
void moveDownSlider() {
  digitalWrite(DIRECTION2, HIGH);
  analogWrite(MOTOR2, 100);
  delay(100);
  analogWrite(MOTOR2, 0);
}
```
### stopSlider
> Stops `MOTOR2`
```cpp
void stopSlider() {
  analogWrite(MOTOR2, 0);
}
```
## Main Loop
> Plays music and runs actuator sequence if confidence is high enough
```cpp
void loop()
{
  if(digitalRead(A3) == LOW) {
    music();
  }else {
    stop1();
    stop2();
  }
  if(digitalRead(SENSE1) == LOW && step == 0 && confidence > 1000 && millis() > 5000) {
    stop1();
    stop2();
    delay(1000);
    moveUpSlider();
    delay(1000);
    pushPencil();
    delay(500);
    stopSlider();
    delay(500);
    moveDownSlider();
    step++;
  }else if(digitalRead(SENSE1) == LOW) {
    confidence++;
  } else {
    confidence = 0;
  }
}
```
