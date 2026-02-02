#Purpose: Convert MIDI files to arduino tones
import mido #midi library

def noteToFreq(note):
    a = 440 #frequency of A (common value is 440Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))

def delay(ms):
    return("delay(" + str(int(ms)) + ");\n")
def noTone():
    return("noTone(BUZZER_PIN);\n")
def tone(freq):
    return("tone(BUZZER_PIN, " + str(int(freq)) + ");\n")

filepath = './midi/MKWCoconutMall.mid' 
mid = mido.MidiFile(filepath)

file = open("output.txt", "w") #output file

track = mid.tracks[1] #selected track
note = 0 # current note register
time = 0 # time counter
reserved = False # Check if there is a note being played



for msg in track:
    time += msg.time # increment time counter
    if (msg.type == 'note_on' or msg.type == 'note_off'): #Make sure the message is a note
        type = (msg.type[5:].upper())
        on = (type == "ON") and msg.velocity > 0 #determine if note is on or off
        if on and not reserved: #begin playing a note
            file.write(delay(time/2))
            time = 0
            note = msg.note
            reserved = True
            file.write(tone(noteToFreq(note)))
        elif not on and reserved and msg.note == note: # stop playing a note
            file.write(delay(time/2))
            time = 0
            file.write(noTone())
            reserved = False
file.close()