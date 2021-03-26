from dmx import Colour, DMXInterface, DMXLight3Slot, DMXLightUking, DMXUniverse
from time import sleep
from sys import exit as sys_exit
import pyaudio
import time
import audioop

RED = Colour(255,0,0)
GREEN = Colour(0,255,0)
BLUE = Colour(0,0,255)
###########################################################################
def get_rms():
    # Creates a generator that can iterate rms values
    CHUNK = 1024
    WIDTH = 2
    CHANNELS = 1
    RATE = 44100
    colourMax = 255

    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=p.get_format_from_width(WIDTH),
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        frames_per_buffer=CHUNK)

        time.sleep(1)
        while True:
            data = stream.read(CHUNK, exception_on_overflow = False)
            rms = audioop.rms(data, 2)
            # Scale the rms value to be within 0-255
            rms_scaled = (rms / 1024) * 255
            if rms_scaled <= colourMax and rms_scaled >= 0:
                yield rms_scaled
    finally:
        p.terminate()
        stream.stop_stream()
        stream.close()

##############################################################################
def set_and_update(universe, interface):
    # update the interface's frame to be the universe's current state
    interface.set_frame(universe.serialise())
    # send and update to the DMX network
    interface.send_update()

##############################################################################
def main():
    # create an instance of the RMS generator
    audio_feed = get_rms()

    # Open an interface
    with DMXInterface("FT232R") as interface:
        # create a universe
        universe = DMXUniverse()

        # define a light
        light = DMXLightUking(address=1)
        light_two = DMXLightUking(address=8)

        # Add the light to a universe
        universe.add_light(light)
        universe.add_light(light_two)

        # Set light to purple
        light.set_brightness(0)
        light_two.set_brightness(0)
        set_and_update(universe, interface)
        
        'create a reset light'
        seq_one = [RED, GREEN, BLUE, RED, RED]
        seq_two = [GREEN, BLUE, RED, BLUE, BLUE]


        for rms in audio_feed:  
            light.set_brightness(rms)
            light.set_colour(GREEN)
            light_two.set_colour(BLUE)
            light_two.set_brightness(rms)
            # set frame and update
            set_and_update(universe, interface)
            #sleep(0.5 - (15.0 / 1000.0))
        
        light.set_brightness(0)
        light_two.set_brightness(0)
        set_and_update(universe, interface)
        return 0

if __name__ == '__main__':
    sys_exit(main())
