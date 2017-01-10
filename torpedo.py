#############################################################
# FILE: torpedo.py
# EXERCISE: intro2cs ex9 2016-2017
# DESCRIPTION: Torpedo class for the game
#############################################################

class Torpedo:
    """
    this is a class for a torpedo
    """
    ACCEL_FACTOR = 2

    def __init__(self, x, y, x_speed, y_speed, heading, radius=4,
                 lifetime=200):
        """
        make the ship with given (x,y) positions
        :param x: staring x position
        :param y: starting y position
        :param heading: starting heading
        :param lifetime : torpedo lifetime (in cycles)
        :param radius: torpedo radius (4 by default)
        """
        self.__x_pos = x
        self.__x_speed = x_speed
        self.__y_pos = y
        self.__y_speed = y_speed
        self.__heading = heading
        self.__radius = radius
        self.__lifetime = lifetime

    def get_position(self):
        """
        get the position
        :return: position as (x,y) tuple
        """
        return self.__x_pos, self.__y_pos

    def set_position(self, x, y):
        """
        sets the position
        torpedo loses one cycle of lifetime when moving
        """
        self.__x_pos = x
        self.__y_pos = y
        self.__lifetime -= 1  # torpedo loses one cycle of lifetime for moving

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

    def get_heading(self):
        """
        :return: heading of the torpedo
        """
        return self.__heading

    def get_radius(self):
        """
        :return: radius of the torpedo
        """
        return self.__radius

    def alive(self):
        """
        checks if torpedo is still alive (has lifetimes cycles left)
        """
        if self.__lifetime > 0:
            return True
        else:
            return False
