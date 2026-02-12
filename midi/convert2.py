import mido

notes1 = []  # Channel 1 (first note)
notes2 = []  # Channel 2 (second note)

def noteToFreq(note):
    a = 440
    return (a / 32) * (2 ** ((note - 9) / 12))

def addNotes(duration, freq1, freq2):
    """Add synchronized note entries to both channels"""
    notes1.append([duration, freq1])
    notes2.append([duration, freq2])

filepath = './midi/MKWCoconutMall.mid' 
mid = mido.MidiFile(filepath)

track = mid.tracks[1]

active_notes = []  # List of currently playing notes [note1, note2]
time = 0

for msg in track:
    time += msg.time
    
    if msg.type == 'note_on' and msg.velocity > 0:
        # Note starts
        if len(active_notes) < 2:
            # Save current state before change
            if time > 0:
                freq1 = int(noteToFreq(active_notes[0])) if len(active_notes) > 0 else 0
                freq2 = int(noteToFreq(active_notes[1])) if len(active_notes) > 1 else 0
                addNotes(int(time/2), freq1, freq2)
                time = 0
            
            active_notes.append(msg.note)
            
            # Start new note
            freq1 = int(noteToFreq(active_notes[0]))
            freq2 = int(noteToFreq(active_notes[1])) if len(active_notes) > 1 else 0
            addNotes(0, freq1, freq2)
            
    elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
        # Note ends
        if msg.note in active_notes:
            # Save duration of previous state
            if time > 0:
                freq1 = int(noteToFreq(active_notes[0])) if len(active_notes) > 0 else 0
                freq2 = int(noteToFreq(active_notes[1])) if len(active_notes) > 1 else 0
                addNotes(int(time/2), freq1, freq2)
                time = 0
            
            active_notes.remove(msg.note)
            
            # Start new state (one less note)
            freq1 = int(noteToFreq(active_notes[0])) if len(active_notes) > 0 else 0
            freq2 = int(noteToFreq(active_notes[1])) if len(active_notes) > 1 else 0
            addNotes(0, freq1, freq2)

# Handle any remaining time
if time > 0:
    freq1 = int(noteToFreq(active_notes[0])) if len(active_notes) > 0 else 0
    freq2 = int(noteToFreq(active_notes[1])) if len(active_notes) > 1 else 0
    addNotes(int(time/2), freq1, freq2)

# Shift timing like original code
for x in range(len(notes1) - 1):
    notes1[x][0] = notes1[x+1][0]
    notes2[x][0] = notes2[x+1][0]

# Write output files
file1 = open("output1.txt", "w")
file1.write("int toneSequence1[][2] = {")
count1 = 0
for x in notes1:
    count1 += 1
    if count1 < 750:
        file1.write("{" + str(x[0]) + ", " + str(x[1]) + "}, ")
file1.write("};")
file1.close()

file2 = open("output2.txt", "w")
file2.write("int toneSequence2[][2] = {")
count2 = 0
for x in notes2:
    count2 += 1
    if count2 < 750:
        file2.write("{" + str(x[0]) + ", " + str(x[1]) + "}, ")
file2.write("};")
file2.close()

print(f"Generated {len(notes1)} synchronized note events")
print(f"Channel 1: output1.txt")
print(f"Channel 2: output2.txt")