#todo-yanir asteriod object intersection

import random
import math

SLOWEST = 1
FASTEST = 5
SIZE_FACTOR = 10
NORMAL = -5

class Asteriod:

    def __init__(self, pos_x, pos_y, size=3):
        """
        Gets position and size and creates an Asteroid object.
        :param pos_x:
        :param pos_y:
        :param size:
        """
        self.__x_pos = pos_x
        self.__y_pos = pos_y
        self.__x_speed = self.random_speed()
        self.__y_speed = self.random_speed()
        self.__ast_size = size
        self.__radius = size * SIZE_FACTOR + NORMAL


    def random_speed(self):
        """
        Returns a random speed between SLOWEST to FASTEST
        :return: speed
        """
        rnd_speed = random.randrange(SLOWEST, FASTEST)
        return rnd_speed

    def get_position(self):
        """
        get the position
        :return: position as (x,y) tuple
        """
        return self.__x_pos, self.__y_pos

    def set_position(self, x, y):
        """
        sets the position
        """
        self.__x_pos = x
        self.__y_pos = y

    def is_in_position(self, pos):
        """
        gets a pos as a tuple and says if the asteroid is at this place
        :param x:
        :param y:
        :return: True if at pos or False if not
        """
        same_place = False
        if self.get_position() == pos:
            same_place = True
        return same_place

    def get_size(self):
        """
        :return: asteroid size
        """
        return self.__ast_size

    def set_size(self, size):
        """
        Set a new size for the asteroid
        :param size:
        """
        self.__ast_size = size

    def get_speed(self):
        """
        get the speed
        :return: speed as (x_speed,y_speed) tuple
        """
        return self.__x_speed, self.__y_speed

    def set_speed(self, x_speed, y_speed):
        """
        sets the speed
        """
        self.__x_speed = x_speed
        self.__y_speed = y_speed

    def get_radius(self):
        """
        :return: radius of the ship
        """
        return self.__radius

    def has_intersection(self, obj):
        """
        Return if there was an intersection between the object and the asteroid
        :param obj:
        :return: True for intersection and False if there wasn't
        """
        obj_x, obj_y = obj.get_position()
        ast_x, ast_y = self.get_position()
        distance = math.sqrt(math.pow(obj_x-ast_x,2)+math.pow(obj_y - ast_y,2))
        result = distance <= self.__radius + obj.get_radius()
        return result
