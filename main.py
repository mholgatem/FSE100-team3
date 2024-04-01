from modules import recorder
import gpiozero
import time, datetime
import argparse
import subprocess
from modules import SQL
from modules.py532lib.i2c import *
from modules.py532lib.frame import *
from modules.py532lib.constants import *


parser = argparse.ArgumentParser(description="NFC Food Tags")

parser.add_argument('-t', dest='record_time', metavar='10', default = 10.0, type = float,
                    help='Time in seconds to record audio')

parser.add_argument('--read', dest='in_read_mode', default=False, action='store_true')

args = parser.parse_args()


class fseProject:
    def __init__(self, args):
        self.args = args #get command line arguments
        self.audio = recorder.InitRecorder() #initialize recorder
        self.recording = False
        SQL.init() #initialize database
        print("In read mode: " + str(self.args.in_read_mode))

        '''
        button stuff
        '''
        # Setup the button & tie it to a function
        self.button = gpiozero.Button(17) #BCM Numbering - physical pin #11
        self.led = gpiozero.LED(26)
        self.button.when_pressed = self.button_stuff

        '''
        nfc stuff 
        '''
        self.pn532 = Pn532_i2c()
        self.pn532.SAMconfigure()

    def button_stuff(self):
        print("Button Pressed!")
        self.recording = True
        self.led.blink(on_time=0.5, off_time=0.5, n=None, background=True)
        card_data = self.scan_nfc()
        tag_id = hex_str = ''.join(f'{byte:02x}' for byte in card_data)
        current_datetime = datetime.datetime.now()
        """SQL.writeTag({"id":None, 
                      "tag_id":tag_id, 
                      "name":"test", 
                      "date":current_datetime.strftime("%H:%M:%S"),
                      "time":current_datetime.strftime("%H:%M:%S"),
                      "audio_file":"./audio/test.wav" })"""
        #recorder.RecordAudio(self.audio, self.args.record_time)
        self.led.off()
        self.led.on()
        time.sleep(7)
        self.led.blink(on_time=0.25, off_time=0.25, n=None, background=True)
        time.sleep(3)
        self.led.off()
        print("TAG: " + str(SQL.getTag(tag_id)))
        self.recording = False
        #return

    def scan_nfc(self):
        card_data = self.pn532.read_mifare().get_data()
        print(''.join(f'{byte:02x}' for byte in card_data))
        return card_data

    def run(self):
        while True:
            try:
                if not self.recording:
                    if self.args.in_read_mode:
                        card_data = self.scan_nfc()
                        tag_id = hex_str = ''.join(f'{byte:02x}' for byte in card_data)
                        tag = SQL.getTag(tag_id)
                        print(str(tag))
                        if tag != None:
                            cmd = 'aplay -r 22050 -f S16_LE -t wav ' + tag['audio_file']
                            print(cmd)
                            subprocess.call( [cmd], executable='/bin/bash', shell=True)
                        
                        time.sleep(5)
                        pass
                time.sleep(0.1)  # Delay to avoid bouncing
            except KeyboardInterrupt:
                self.cleanup()
            #except:
                #self.cleanup()
                    
    def cleanup(self):
        SQL.sqlCursor.close()
        SQL.SQL.close()

if __name__ == "__main__":
    daemon = fseProject(args)
    daemon.run()
