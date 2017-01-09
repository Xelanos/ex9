#todo-yanir asteriod init
#todo-yanir asteriod object intersection
#todo-yanir radius

class Asteriod:

    def __init__(self, pos_x, pos_y, size=3):
        """
        Gets position and size and creates an Asteroid object.
        :param pos_x:
        :param pos_y:
        :param size:
        """
        self.__ast_pos_x = pos_x
        self.__ast_pos_y = pos_y
        self.__ast_size = size

    def get_position(self):
        """
        get the position
        :return: position as (x,y) tuple
        """
        return self.__ast_pos_x, self.__ast_pos_y

    def set_position(self, x, y):
        """
        sets the position
        """
        self.__ast_pos_x = x
        self.__ast_pos_xy = y

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