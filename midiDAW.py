# Hi, I need to communicate with your digital audio workstation to send MIDI to it
from simplecoremidi import send_midi, MIDISource
import socket             

class MIDI_DAW:
    def __init__(self, name:str):
        self.source = MIDISource(name)

    def convert_midi2_0_to_midi1_0_sm(self, pkt):
        status  = pkt[8:12]
        channel = pkt[12:16]
        index   = pkt[16:32]
        data    = pkt[32:]
        b1 = 0x0
        b2 = 0x0
        b3 = 0x0

        channel = int(channel, 2)

        if status == "1000":
            #note off
            b1 = 0x80 | channel
            b2 = int(index[:8], 2)
            if '1' in data[:8]:
                b3 = 0xff
            else:
                b3 = int(data[8:16], 2)
        elif status == "1001":
            #note on
            b1 = 0x90 | channel
            b2 = int(index[:8], 2)
            if '1' in data[:8]:
                b3 = 0xff
            else:
                b3 = int(data[8:16], 2)
        elif status == "1010":
            #key pressure
            b1 = 0xA0 | channel
            b2 = int(index[:8], 2)
            if '1' in data[:8]:
                b3 = 0xff
            else:
                b3 = int(data, 2)
        elif status == "1011":
            #cc
            b1 = 0xB0 | channel
            b2 = int(index[:8], 2)
            if '1' in data[:24]:
                b3 = 0xff
            else:
                b3 = int(data, 2)
        elif status == "1100":
            #program change
            b1 = 0xC0 | channel
            b2 = int(data[:8], 2)
        elif status == "1101":
            #channel pressure
            b1 = 0xD0 | channel
            b2 = int(data[:8], 2)
        elif status == "1110":
            #pitch bend
            b1 = 0xE0 | channel
            b2 = int(data[:8], 2)
            b3 = int(data[8:16], 2)
        # print ('b1: ', b1)
        # print ('b2: ', b2)
        # print ('b3: ', b3)
        self.source.send((b1, b2, b3))

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host, port = "127.0.0.1", 5009  

  # with socket.socket() as s:
  s.connect((host, port))
  while True:
      rec = str(s.recv(1024).decode('utf-8'))
      print (rec)
      if rec == '':
        continue
      if int(rec) == 0:
        s.close()
        break
      try:
          convert_midi2_0_to_midi1_0_sm(rec)
      except Exception as e:
          print (str(e))
          # s.close()
          break
      
      # s.close()                     # Close the socket when done


