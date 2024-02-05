#Code copied from a previous project that I've made

import math #Import required module

class Vector:

    def __init__(self, x, y):
        """
        Represents a Vector object

        Attributes
            x (num): x coord
            y (num): y coord
        """
        self.x = x
        self.y = y

    def coord(self):
        """Returns the coord in tuple form"""
        return (self.x, self.y)

    def __add__(self, num):
        """
        Add vectors together
        Args:
            num (Vector object/num)
        Returns:
            (Vector object)
        """

        if isinstance(num, Vector):
            x = self.x + num.x
            y = self.y + num.y
        else:
            x = self.x + num
            y = self.y + num
        return Vector(x, y)

    def __sub__(self, num):
        """
        Subtract the vectors
        Args:
            num (Vector object/num)
        Returns:
            (Vector object)
        """

        if isinstance(num, Vector):
            x = self.x - num.x
            y = self.y - num.y
        else:
            x = self.x - num
            y = self.y - num
        return Vector(x, y)

    def __mul__(self, num):
        """
        Multiply vectors together
        Args:
            num (Vector object/num)
        Returns:
            (Vector object)
        """

        if isinstance(num, Vector):
            x = self.x * num.x
            y = self.y * num.y
        else:
            x = self.x * num
            y = self.y * num
        return Vector(x, y)

    def __truediv__(self, num):
        """
        Divide two vectors
        Args:
            num (Vector object/num)
        Returns:
            (Vector object)
        """

        if isinstance(num, Vector):
            x = self.x / num.x
            y = self.y / num.y
        else:
            x = self.x / num
            y = self.y / num
        return Vector(x, y)
    
    def __eq__(self, other):
        """
        Check if two vectors equal eachother
        Args:
            num (Vector object)
        Returns:
            (bool)
        """
        return self.x == other.x and self.y == other.y

    def round(self):
        """Round the numbers in the vector"""
        self.x = round(self.x)
        self.y = round(self.y)
        return self

    def distance(self, vector):
        """
        Check the distance between two vectors
        Args:
            vector (Vector object)
        Returns:
            (num)
        """
        return math.sqrt(((self.x - vector.x)**2) + ((self.y - vector.y)**2))
