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
        :param radius: ships radius (4 by default)
        """
        self.__x_pos = x
        self.__x_speed = x_speed
        self.__y_pos = y
        self.__y_speed = y_speed
        self.__heading = heading
        self.__radius = radius
        self.__lifetime = lifetime

    def get_position(self):
        return self.__x_pos, self.__y_pos

    def set_position(self, x, y):
        self.__x_pos = x
        self.__y_pos = y
        self.__lifetime -= 1  # torpedo loses one cycle of lifetime for moving

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

    def alive(self):
        if self.__lifetime > 0:
            return True
        else:
            return False
