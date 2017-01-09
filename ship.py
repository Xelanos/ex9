from math import sin, cos, radians
from torpedo import Torpedo

FULL_CIRCLE = 360


class Ship:
    """
    this is a class for a ship
    """
    ACCEL_FACTOR = 1

    def __init__(self, x, y, heading=0, starting_life=3, radius=1):
        """
        make the ship with given (x,y) positions
        :param x: staring x position
        :param y: starting y position
        :param heading: starting heading (0 by default)
        :param starting_life: 3 by default
        :param radius: ships radius (1 by default)
        """
        self.__x_pos = x
        self.__y_pos = y
        self.__x_speed = 0   # every ship starts stationary
        self.__y_speed = 0   # every ship starts stationary
        self.__heading = float(heading)
        self.__life = starting_life
        self.__radius = radius

    def get_position(self):
        return self.__x_pos, self.__y_pos

    def set_position(self, x, y):
        self.__x_pos = x
        self.__y_pos = y

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def set_speed(self, x_speed, y_speed):
        self.__x_speed = x_speed
        self.__y_speed = y_speed

    def get_heading(self):
        return self.__heading

    def get_radius(self):
        return self.__radius

    def ship_drawing_parameters(self):
        return self.__x_pos, self.__y_pos, self.__heading

    def change_direction(self, angle):
        """
        changes current ship heading by 'angle' degrees
        :param angle: an int from -360 to 360
        """
        new_heading = self.__heading + angle
        if new_heading >= 0:
            self.__heading = new_heading
        else:
            self.__heading = FULL_CIRCLE + new_heading

    def fire_torpedo(self):
        """
        fire a torpedo from the tip of the ship
        :return:
        """
        torpedo = Torpedo(*self.get_position(), *self.get_speed(),
                          self.get_heading())
        return torpedo


    def lose_a_life(self):
        """
        subtract one life from current ship life amount
        :return: if ship is dead return
        """
        self.__life -= 1
        if self.__life < 1:
            return #todo-or game lost