from saveable.saveable import SaveableType
import struct


class SaveableFloat(SaveableType):
    """
    A saveable int type that can be saved as a c-type specified in struct
    """

    def __init__(self, value=0):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def load_in_place(self, byte_array):
        self.value = struct.unpack('<f', byte_array[:4])[0]
        for x in range(4):
            byte_array.pop(0)

    def to_byte_array(self):
        return bytearray(struct.pack('<f', self.value))

    def __str__(self):
        return str(self.value)
