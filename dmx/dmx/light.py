"""Module for DMX light definitions."""
from abc import ABC, abstractmethod
from typing import List

from dmx.colour import BLACK, Colour

DMX_MAX_ADDRESS = 512
DMX_MIN_ADDRESS = 1


class DMXLight(ABC):
    """Represents a DMX light."""

    def __init__(self, address: int = 1):
        """Initialise the light. The base initialiser simply stores the address."""
        self._address = int(max(0, min(address, DMX_MAX_ADDRESS)))

    @abstractmethod
    def serialise(self) -> List[int]:
        """Serialise the DMX light to a sequence of bytes."""

    @property
    def start_address(self) -> int:
        """Start address (inclusive) of the light."""
        return self._address

    @property
    def end_address(self) -> int:
        """End address (inclusive) of the light."""
        end_address = self._address + self.slot_count - 1
        if end_address > DMX_MAX_ADDRESS or end_address < DMX_MIN_ADDRESS:
            return (end_address % DMX_MAX_ADDRESS) + DMX_MIN_ADDRESS
        return end_address

    @property
    def slot_count(self) -> int:
        """Get the number of slots used by this light."""
        return 0


class DMXLight3Slot(DMXLight):
    """Represents a DMX light with RGB."""

    def __init__(self, address: int = 1):
        """Initialise the light."""
        super().__init__(address=address)
        self._colour = BLACK

    @property
    def slot_count(self) -> int:
        """Get the number of slots used by this light."""
        return 3

    def set_colour(self, colour: Colour):
        """Set the colour for the light."""
        self._colour = colour

    def serialise(self) -> List[int]:
        """Serialise the DMX light to a sequence of bytes."""
        return self._colour.serialise()


class DMXLight7Slot(DMXLight3Slot):
    """Represents an DMX light with RGB, rotation, and opacity."""

    def __init__(self, address: int = 1):
        """Initialise the light."""
        super().__init__(address=address)
        self._opacity = 255
        self._coords = (0, 0, 0)

    def set_rotation(self, pitch: int, roll: int, yaw: int):
        """Set the rotation of the light, each value between 0 and 255 (inclusive)."""
        pitch = int(max(0, min(pitch, 255)))
        roll = int(max(0, min(roll, 255)))
        yaw = int(max(0, min(yaw, 255)))
        self._coords = (pitch, roll, yaw)

    def set_opacity(self, value: int):
        """Set the opacity of the light between 0 and 255 (inclusive)."""
        self._opacity = int(max(0, min(value, 255)))

    @property
    def slot_count(self) -> int:
        """Get the number of slots used by this light."""
        return 7

    def serialise(self) -> List[int]:
        """Serialise the DMX light to a sequence of bytes."""
        return super().serialise() + list(self._coords) + [self._opacity]



# new class for me
class DMXLightUking(DMXLight3Slot):
    ''' Represents a Uking DMX light'''

    def __init__(self, address: int = 1):
        '''Initialise the light.'''
        super().__init__(address=address)
        self._brightness = 255
        self._strobe = 0
        self._preset_one = 0
        self._preset_two = 0

    def set_brightness(self, value: int):
        '''Set the brightness of the light between 0 and 255'''
        self._brightness = int(max(0, min(value, 255)))

    def set_strobe(self, value: int):
        '''Set the of the light'''
        self._strobe = int(max(0, min(value, 255)))

    def set_preset_one(self, value: int):
        '''Set the first preset slot'''
        self._preset_one = int(max(0, min(value, 255)))

    def set_preset_two(self, value: int):
        '''Set the second preset slot'''
        self._preset_two = int(max(0, min(value, 255)))

    @property
    def slot_count(self) -> int:
        '''Get the number of slots used by this light.'''
        return 7

    def serialise(self) -> List[int]:
        '''Serialise the DMX light to a sequence of bytes'''
        return [self._brightness] + super().serialise() + [self._strobe] + [self._preset_one] + [self._preset_two]










