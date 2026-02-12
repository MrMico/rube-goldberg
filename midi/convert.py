#Purpose: Convert MIDI files to arduino tones
import mido #midi library

notes = []

def noteToFreq(note):
    a = 440 #frequency of A (common value is 440Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))

def delay(ms):
    notes.append([ms, 0])
def noTone():
    notes[-1][1] = -1
def tone(freq):
    notes[-1][1] = int(freq)

filepath = './midi/MKWCoconutMall.mid' 
mid = mido.MidiFile(filepath)

file = open("output.csv", "w") #output file
file2 = open("output2.txt", "w")

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
            delay(time/2)
            time = 0
            note = msg.note
            reserved = True
            tone(noteToFreq(note))
            
        elif not on and reserved and msg.note == note: # stop playing a note
            delay(time/2)
            time = 0
            noTone()
            reserved = False
file.close()

for x in range(0, len(notes)-1):
    notes[x][0] = notes[x+1][0]

file2.write("int toneSequence[][2] = {")
for x in notes:
    file2.write("{" + str(x[0]) + ", " + str(x[1]) + "}, ")
file2.write("};")
file2.close()