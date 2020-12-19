from dmx import Colour, DMXInterface, DMXLight3Slot, DMXLightUking, DMXUniverse
from time import sleep
from sys import exit as sys_exit
import random

# blue colour scheme 
CYAN = Colour(0,255,208)
GREEN = Colour(0,255,81)
BLUE = Colour(0,174,255)
blue_scheme = [CYAN, GREEN, BLUE]

# red colour scheme
RED = Colour(255,0,47)
ORANGE = Colour(255,81,0)
PINK = Colour(255,0,175)
red_scheme = [RED, ORANGE, PINK]

##############################################################################
def set_and_update(universe, interface):
    # update the interface's frame to be the universe's current state
    interface.set_frame(universe.serialise())
    # send and update to the DMX network
    interface.send_update()

##############################################################################
def blackout(lights):
    for light in lights:
        light.reset()
    
##############################################################################

def main():
    
    # Open an interface
    with DMXInterface("FT232R") as interface:
        # create a universe
        universe = DMXUniverse()

        # define a light
        lights = []
        for i in range(64):
            light = DMXLightUking(address=1 + (7 * i))
            lights.append(light)
            universe.add_light(light)

        # make sure all lights are reset
        blackout(lights)
        set_and_update(universe, interface)

        # To Do
        # infinite loop that checks for updates from max
        # if update
        #     read seq file selection
        #     set exe time
        #  once equals exe time
        #     for command in seq file
        #         set lights
        # 
        # 
        #
        #  
        sleep(0.5 - (15.0 / 1000.0))
       
        
        # before exiting blackout
        blackout(lights)
        set_and_update(universe, interface)
        return 0

if __name__ == '__main__':
    sys_exit(main())
