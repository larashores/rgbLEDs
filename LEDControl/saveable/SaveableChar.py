from saveable.saveable import SaveableType
import struct


class SaveableChar(SaveableType):
    """
    A saveable int type that can be saved as a c-type specified in struct
    """

    def __init__(self, value='a'):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        if not (type(value) == str and len(value) == 1):
            raise ValueError('Must be 1 character string ({})'.format(value))
        self.value = value

    def load_in_place(self, byte_array):
        self.value = struct.unpack('<c', byte_array[0:1])[0].decode('ascii')
        byte_array.pop(0)

    def to_byte_array(self):
        return struct.pack('<c', self.value.encode('ascii'))

    def __str__(self):
        return str(self.value)



def unpackChar(data):
    char = struct.unpack('c',bytes( (data[0],) ) )
    data.pop(0)
    return char[0].decode('ascii')
