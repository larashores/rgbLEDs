from abc import abstractmethod, ABCMeta


class SaveableType(metaclass=ABCMeta):
    """
    Type used to specify a type of object that can be converted to a bytearray and pops the data off the bytearray
    """

    @classmethod
    def from_byte_array(cls, byte_array):
        """
        Makes a new Component object from a bytearray

        Args:
            byte_array:   The bytearray representing the object

        Returns:
            A Component object
        """
        obj = cls()
        obj.load_in_place(byte_array)
        return obj

    @abstractmethod
    def to_byte_array(self):
        """
        Return a bytearray representation of the Component

        Returns:
            The bytearray
        """
        return bytearray()

    @abstractmethod
    def load_in_place(self, byte_array):
        """
        Given a byte array, loads all values of the saveable object and pops the data off the bytearray

        Args:
            byte_array: The bytearray to load
        """
        pass

    def copy(self):
        new = type(self)()
        new.load_in_place(self.to_byte_array())
        return new

