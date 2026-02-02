#Purpose: Convert MIDI files to arduino tones
import mido

def noteToFreq(note):
    a = 440 #frequency of A (common value is 440Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))

filepath = './midi/MKWCoconutMall.mid'
mid = mido.MidiFile(filepath)

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))

file = open("output.txt", "w")


print("start")
piano = mid.tracks[1]
note = 0
time = 0
reserved = False
for i, msg in enumerate(piano):
    if i > 0:
        if (msg.type == 'note_on' or msg.type == 'note_off'):
            #print(msg.note, msg.time, msg.type)
            type = (msg.type[5:].upper())
            on = (type == "ON") and msg.velocity > 0
            time += msg.time
            if on and not reserved:
                print("delay(", int(time/2), ");")
                file.write("delay(" + str(int(time/2)) + ");\n")
                time = 0
                note = msg.note
                reserved = True
                file.write("tone0.play(" + str(int(noteToFreq(note))) + ");\n")
            elif not on and reserved and msg.note == note:
                print("delay(", int(time/2), ");")
                
                file.write("delay(" + str(int(time/2)) + ");\n")
                time = 0
                print("noTone(BUZZER_PIN);")
                file.write("tone0.stop();\n")
                reserved = False

        else:
            print(msg)
file.close()