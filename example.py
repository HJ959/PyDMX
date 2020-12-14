from dmx import Colour, DMXInterface, DMXLight3Slot, DMXLightUking, DMXUniverse
from time import sleep
from sys import exit as sys_exit
import random

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
    random.seed()

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
        light.reset()
        light.set_brightness(0)
        light_two.set_brightness(0)
        set_and_update(universe, interface)
        
        'create a reset light'
        seq_one = [RED, GREEN, BLUE, RED, RED]
        seq_two = [GREEN, BLUE, RED, BLUE, BLUE]

        r_num_1 = random.randint(0,255)
        r_num_2 = random.randint(0,255)
        r_num_3 = random.randint(0,255)
        random_colour = Colour(r_num_1,r_num_2,r_num_3)

        
        print('Wait one second and go!')
        sleep(1)

        b_value = 0
        for _ in range(0,500):
            light.set_preset_one(113)
            light.set_preset_speed(20)
            light.set_colour(random_colour)
            
            light_two.set_preset_one(121)
            light_two.set_preset_speed(20)
            light_two.set_brightness(b_value)
            
            # set frame and update
            set_and_update(universe, interface)
            
            sleep(0.5 - (15.0 / 1000.0))
            b_value += 20
            b_value %= 255
        
        # turn all params to 0
        light.reset()
        light_two.reset()

        set_and_update(universe, interface)
        return 0

if __name__ == '__main__':
    sys_exit(main())
