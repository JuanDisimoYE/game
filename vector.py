from copy import deepcopy
from math import sin, cos, sqrt, pow, pi, atan, asin, acos
from test_functions import get_line

class vector:
    def __init__(self, direction, length):
        self.direction = deepcopy(direction)
        self.length = deepcopy(length)

    def get_length(self):
        return deepcopy(self.length)
    
    def get_direction(self):
        return deepcopy(self.direction)
    
    def set_length(self, length):
        self.length = deepcopy(length)

    def set_direction(self, direction):
        self.direction = deepcopy(direction)

    def get_scalar_vector(self) -> list:
        x_vector = self.get_length() * sin(self.get_direction())
        y_vector = self.get_length() * cos(self.get_direction())
        return [x_vector, y_vector]
    
    def set_scalar_vector(self, scalar_vector:tuple) -> None:
        self.direction = get_angle_of_vector((0,0), scalar_vector)
        self.length = __get_length(scalar_vector)


    

def add_vector(vector_1:vector, vector_2:vector) -> vector:
    x_length = vector_1.get_length()*sin(vector_1.get_direction()) + vector_2.get_length()*sin(vector_2.get_direction())
    y_length = vector_1.get_length()*cos(vector_1.get_direction()) + vector_2.get_length()*cos(vector_2.get_direction())
    length = __get_length((x_length, y_length))
    direction = __arctan(y_length, x_length)
    return vector(direction, length)

def get_angle_of_vector(origin:list, destination:list):
    x = destination[0] - origin[0]
    y = destination[1] - origin[1]
    length = __get_length( (x, y) )
    if x >= 0:
        angle = acos(y/length)
    else:
        angle = acos(-y/length) + pi

    return angle

def __get_length(vector:tuple):
    return sqrt( pow(vector[0], 2) + pow(vector[1], 2) )

def __arctan(ankathete, gegenkathete):
    if ankathete == 0:
        angle = pi/2
    else:
        angle = atan(gegenkathete / ankathete)
    return angle

def __deg_to_rad(deg):
    rad = deg * (pi / 180)
    return rad













if __name__ == "__main__":
    test_vector_1 = vector(__deg_to_rad(30), 1)
    test_vector_2 = vector(__deg_to_rad(150), 1)
    test_vector_3 = vector(__deg_to_rad(330), 1)
    test_vector_4 = vector(__deg_to_rad(210), 1)

    if ( test_vector_1.get_scalar_vector()[0] - test_vector_2.get_scalar_vector()[0] ) > 0.01: print(f"error in line {get_line()}")
    if ( test_vector_3.get_scalar_vector()[0] - test_vector_4.get_scalar_vector()[0] ) > 0.01: print(f"error in line {get_line()}")

    if ( abs(test_vector_1.get_scalar_vector()[1]) - abs(test_vector_3.get_scalar_vector()[1]) ) > 0.01: print(f"error in line {get_line()}")
    if ( abs(test_vector_2.get_scalar_vector()[1]) - abs(test_vector_4.get_scalar_vector()[1]) ) > 0.01: print(f"error in line {get_line()}")


    if abs(get_angle_of_vector((0,0), (1,1)) - __deg_to_rad(45)) > 0.01: print(f"error in line {get_line()}")
    if abs(get_angle_of_vector((0,0), (1,-1)) - __deg_to_rad(135)) > 0.01: print(f"error in line {get_line()}")
    if abs(get_angle_of_vector((0,0), (-1,-1)) - __deg_to_rad(225)) > 0.01: print(f"error in line {get_line()}")
    if abs(get_angle_of_vector((0,0), (-1,1)) - __deg_to_rad(315)) > 0.01: print(f"error in line {get_line()}")

    print("vector test done")
