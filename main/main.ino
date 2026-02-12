#include "pitches.h"
#include "analogWave.h" // Include the library for analog waveform generation
#define BUZZER_PIN 3

analogWave wave(DAC);   // Create an instance of the analogWave class, using the DAC pin

int b1Duration = 0;
int b2Duration = 0;
int cycle1 = 0;
int cycle2 = 0;
int length = 750;
int reset = 0;

void setup() {
  Serial.begin(9600);
  wave.square(10);
  wave.stop();
  pinMode(BUZZER_PIN, OUTPUT);
}


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

int newMillis() {
  return millis() - reset;
}

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

void loop()
{
  music();
  //Do other stuff
}