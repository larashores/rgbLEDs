from .model import *


def save(pattern, path):
    """
    Takes a runner pattern and saves it to the end of a file
    """
    with open(path, 'wb') as file:
        file.write(pattern.to_byte_array())


def load(path):
    with open(path, 'rb') as file:
        data = bytearray(file.read())
        return RunnerPattern.from_byte_array(data)
