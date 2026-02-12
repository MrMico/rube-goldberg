// Micah Jabbour and Joshua Haupt
// February 2, 2026
// Midi for dual-buzzer arduino output


int BUZZER_PIN = 11;
int b1Duration = 0;
int b2Duration = 0;
int cycle = 0;
int toneSequence[500][2];

void setup()
{

}

void loop()
{
  // change note when duration of note is over
  if (b1Duration >= millis()) {
    // set next note duration
    b1Duration = millis() + toneSequence[cycle][0];
    cycle++;

    // set next note
    if (toneSequence[cycle][1] > 0) {
      tone(BUZZER_PIN, toneSequence[cycle][1]);
    }
    else {
      // if the value of the note is -1, play no sound (rest)
      noTone(BUZZER_PIN);
    }
  }
}
