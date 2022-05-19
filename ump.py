def b2(input):
    return bin(input)[2:]

class UniversalMIDIPacket:
    def __init__(self, name, message_type, group, status, index=None, data=None):
        self.name = name
        self.message_type = message_type
        self.group = group
        self.status = status 
        self.index = index
        self.data = data

    def packet_to_binary(self):
        start = b2(self.message_type).zfill(4) + b2(self.group).zfill(4) 
        end = ""
        if self.message_type == 0:
            end = b2(self.status).zfill(4) + b2(self.data).zfill(20)
        elif self.message_type == 2:
            end = b2(self.status).zfill(8)
            if (self.index is None):
                end += b2(self.data).zfill(16)
            else:
                end += b2(self.index).zfill(8) + b2(self.data).zfill(8)
        elif self.message_type == 4:
            end = b2(self.status).zfill(8) + b2(self.index).zfill(16) + b2(self.data).zfill(32)
        return start + end

    def __str__(self):
        return self.name + '\n' + self.packet_to_binary()

class MIDIMessageCreator:
    def __init__(self):
        pass

    def midi1_0_note_off(note_num, vel, group=0, channel=0):
        data = note_num << 8 | vel
        status = int("1000", 2)
        ch = int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Note Off Message", 2, group, status << 4 | ch, data=data)

    def midi1_0_note_on(note_num, vel, group=0, channel=0):
        data = note_num << 8 | vel
        status = int("1001", 2)
        ch = int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Note On Message", 2, group, status << 4 | ch, data=data)

    def midi1_0_poly_pressure(note_num, data, group=0, channel=0):
        status = int("1010", 2)
        ch = bin(channel)
        return UniversalMIDIPacket("MIDI 1.0 Poly Pressure Message", 2, group, status << 4 | ch, data=note_num << 8 | data)

    def midi1_0_cc(index, data, group=0, channel=0):
        status = int("1011", 2)
        ch = int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Control Change Message", 2, group, status << 4 | ch, index=index, data=data)

    def midi1_0_program_change(program, group=0, channel=0):
        data = {"program": program}
        status = int("1100", 2)
        ch = int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Program Change Message", 2, group, status << 4 | ch, data=data)

    def midi1_0_pitch_bend(lsb_data, msb_data, group=0, channel=0):
        data = lsb_data << 8 | msb_data
        status = int("1110", 2)
        ch = int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Pitch Bend Message", 2, group, status << 4 | ch, data=data)
        
    def midi2_0_note_off(note_num, atr_type, vel, atr_data=0, group=0, channel=0):
        ch = int(channel)
        status = int('1000', 2)
        return UniversalMIDIPacket("MIDI 2.0 Note Off Message", 4, group, status << 4 | ch, index = int(note_num) << 8 | int(atr_type), 
                                    data = int(vel) << 16 | int(atr_data))

    def midi2_0_note_on(note_num, atr_type, vel, atr_data=0, group=0, channel=0):
        ch = int(channel)
        status = int('1001', 2)
        return UniversalMIDIPacket("MIDI 2.0 Note On Message", 4, group, status << 4 | ch, index = (int(note_num)) << 8 | (int(atr_type)), 
                                    data = (vel) << 16 | (atr_data))

    def midi2_0_poly_pressure(note_num, data, group=0, channel=0):
        reserved = 0
        ch = int(channel)
        status = int('1010', 2)
        return UniversalMIDIPacket("MIDI 2.0 Poly Pressure Message", 4, group, status << 4 | ch, index = int(note_num) << 8 | reserved, 
                                    data = data)

    def midi2_0_reg_per_note(note_num, index, data, group=0, channel=0):
        ch = int(channel)
        status = int('0000', 2)
        return UniversalMIDIPacket("MIDI 2.0 Registered Per-Note Controller Message", 4, group, status << 4 | ch, index = int(note_num) << 8 | int(index), 
                                    data = data)

    def midi2_0_asn_per_note(note_num, index, data, group=0, channel=0):
        ch = int(channel)
        status = int('0001', 2)
        return UniversalMIDIPacket("MIDI 2.0 Assignable Per-Note Controller Message", 4, group, status << 4 | ch, index = int(note_num) << 8 | int(index), 
                                    data = data)

    def midi2_0_per_note_management(note_num, d, s, group=0, channel=0):
        reserved = 0
        ch = int(channel)
        status = int('1111', 2)
        return UniversalMIDIPacket("MIDI 2.0 Per-Note Management Message", 4, group, status << 4 | ch, index = int(note_num) << 8 | d << 1 | s, data = reserved)

    def midi2_0_cc(index, data, group=0, channel=0):
        reserved = int(0)
        ch = int(channel)
        status = int("1011", 2)
        return UniversalMIDIPacket("MIDI 2.0 Control Change Message", 4, group, status<<4 | ch, index = index << 8 | reserved, data=data)

    def midi2_0_reg_controller(bank, index, data, group=0, channel=0):
        ch = int(channel)
        status = int("0010", 2)
        return UniversalMIDIPacket("MIDI 2.0 Registered Controller Message", 4, group, status<<4 | ch, index = bank << 8 | index, data=data)

    def midi2_0_asn_controller(bank, index, data, group=0, channel=0):
        ch = int(channel)
        status = int("0011", 2)
        return UniversalMIDIPacket("MIDI 2.0 Assignable Controller Message", 4, group, status<<4 | ch, index = bank << 8 | index, data=data)

    def midi2_0_rel_reg_controller(bank, index, data, group=0, channel=0):
        ch = int(channel)
        status = int("0100", 2)
        return UniversalMIDIPacket("MIDI 2.0 Relative Registered Controller Message", 4, group, status<<4 | ch, index = bank << 8 | index, data=data)

    def midi2_0_rel_asn_controller(bank, index, data, group=0, channel=0):
        ch = int(channel)
        status = int("0101", 2)
        return UniversalMIDIPacket("MIDI 2.0 Relative Assignable Controller Message", 4, group, status<<4 | ch, index = bank << 8 | index, data=data)

    def midi2_0_program_change(b, program, bank_msb, bank_lsb, group=0, channel=0):
        reserved = 0
        ch = int(channel)
        status = int("1100", 2)
        return UniversalMIDIPacket("MIDI 2.0 Program Change Message", 4, group, status<<4 | ch, index = reserved << 8 | b, data=program << 24 | reserved << 16 | bank_msb << 8 | bank_lsb)
    
    def midi2_0_channel_pressure(data, group=0, channel=0):
        reserved = 0
        ch = int(channel)
        status = int("1101", 2)
        return UniversalMIDIPacket("MIDI 2.0 Channel Pressure Message", 4, group, status<<4 | ch, index = reserved << 8 | reserved, data=data)
    
    def midi2_0_pitch_bend(data, group=0, channel=0):
        reserved = 0
        ch = int(channel)
        status = int("1110", 2)
        return UniversalMIDIPacket("MIDI 2.0 Pitch Bend Message", 4, group, status<<4 | ch, index = reserved << 8 | reserved, data=data)
