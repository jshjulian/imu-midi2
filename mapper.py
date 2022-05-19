import json, ump, midiDAW

def map_params(controller, synth):
    params = {}
    for p in controller['ControllerParameters']:
        print (synth['ControllerParameters'])
        x = input("Which param do you want to link with ", p)
        if x == "":
            continue
        params[p] = {"Controls": x}
        y = input("cc or noteon")
        if y == 'cc' or y == 'noteon':
            params[p]['MessageType'] = y
        if y == 'cc':
            z = input("What is the CC number?: ")
        else:
            z = input("What is the MIDI Note number?: ")
        params[p]["Number"] = z
        print ("Adjust the parameter in your DAW, then press Enter")
        if y == 'cc':
            msg = ump.MIDIMessageCreator.midi2_0_cc(z, 0)
            midiDAW.convert_midi2_0_to_midi1_0_sm(msg.packet_to_binary())
        else:
            msg = ump.MIDIMessageCreator.midi2_0_note_on(z, 0, 127)
            midiDAW.convert_midi2_0_to_midi1_0_sm(msg.packet_to_binary())
            msg = ump.MIDIMessageCreator.midi2_0_note_off(z, 0, 127)
            midiDAW.convert_midi2_0_to_midi1_0_sm(msg.packet_to_binary())
    
    with open('mapping.json', 'w') as fp:
        json.dump(params, fp)
    
    return params

if __name__ == "__main__":
    with open('harmless.json') as json_file:
        harmless = json.load(json_file)
    with open('snaclo.json') as json_file:
        snaclo = json.load(json_file)
    result = map_params(snaclo, harmless)
    print (result)