import math


# Vector class representing a 2D vector
class Vector(object):
    # Constructor to initialize the vector with default values or specified values
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Overloaded addition operator for vector addition
    def __add__(self, next):
        return Vector(self.x + next.x, self.y + next.y)

    # Overloaded subtraction operator for vector subtraction
    def __sub__(self, next):
        return Vector(self.x - next.x, self.y - next.y)

    # Overloaded negation operator for negating the vector
    def __neg__(self):
        return Vector(-self.x, -self.y)

    # Overloaded multiplication operator for scalar multiplication
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # Overloaded division operator for scalar division
    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector(self.x / float(scalar), self.y / float(scalar))
        return None

    # Method to calculate the squared Magnitude of the vector
    def vectorMagnitudeSqr(self):
        return self.x**2 + self.y**2

    # Method to create a copy of the vector
    def vectorCopy(self):
        return Vector(self.x, self.y)

    # Method to represent the vector as a tuple
    def vectorTuple(self):
        return self.x, self.y

    # Method to represent the vector as integers
    def vectorInt(self):
        return int(self.x), int(self.y)
