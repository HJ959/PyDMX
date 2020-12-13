from dmx import Colour, DMXInterface, DMXLight3Slot, DMXLightUking, DMXUniverse
from time import sleep
from sys import exit as sys_exit

RED = Colour(255,0,0)
GREEN = Colour(0,255,0)
BLUE = Colour(0,0,255)
##############################################################################
def set_and_update(universe, interface):
    # update the interface's frame to be the universe's current state
    interface.set_frame(universe.serialise())
    # send and update to the DMX network
    interface.send_update()

##############################################################################
def main():
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


        for _ in range(0,50):  
            light.set_brightness(255)
            light.set_colour(GREEN)
            light_two.set_colour(BLUE)
            light_two.set_brightness(255)
            # set frame and update
            set_and_update(universe, interface)
            sleep(0.5 - (15.0 / 1000.0))
        
        light.set_brightness(0)
        light_two.set_brightness(0)
        set_and_update(universe, interface)
        return 0

if __name__ == '__main__':
    sys_exit(main())
