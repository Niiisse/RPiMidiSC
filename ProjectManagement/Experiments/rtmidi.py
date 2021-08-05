import rtmidi

midiin = rtmidi.RtMidiIn()

def print_message(midi):
    if midi.isNoteOn():
        print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())

ports = range(midiin.getPortCount())
if ports:
    for i in ports:
        print(midiin.getPortName(i))
    print("Opening port 0!") 
    midiin.openPort(0)
    while True:
        m = midiin.getMessage(250) # some timeout in ms
        if m:
            print_message(m)
else:
    print('NO MIDI INPUT PORTS!')