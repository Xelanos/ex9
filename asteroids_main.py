import random
import sys
from math import sin, cos, radians
from screen import Screen
from ship import Ship
from torpedo import Torpedo


DEFAULT_ASTEROIDS_NUM = 5
RIGHT = -7
LEFT = 7


class GameRunner:

    def __init__(self, asteroids_amnt):
        #todo-yanir add asteriods
        self._screen = Screen()
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self._ship = Ship(self.random_coordinate(), self.random_coordinate())
        self._torpedoes = []

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def accelerate_object(self, obj):
        """
        accelerate the object withing the game by the laws
        :param obj: an object in the game
        :return:
        """
        current_x_speed, current_y_speed = obj.get_speed()
        new_x_speed = current_x_speed +\
                      (obj.ACCEL_FACTOR * cos(radians(obj.get_heading())))
        new_y_speed = current_y_speed + \
                      (obj.ACCEL_FACTOR * sin(radians(obj.get_heading())))
        obj.set_speed(new_x_speed, new_y_speed)


    def move_object(self, obj):
        """
        moves an object withing the game.
        function assumes object has get_position function that returns a
        tuple of (x,y) coordinates and get_speed with the same return values.
        also assume object has a position setter
        """
        old_x, old_y = obj.get_position()
        x_speed, y_speed = obj.get_speed()
        delta_axis = self.screen_max_x - self.screen_min_x
        new_x = (x_speed + old_x - self.screen_min_x) % delta_axis\
                + self.screen_min_x
        new_y = (y_speed + old_y - self.screen_min_y) % delta_axis\
                + self.screen_min_y
        obj.set_position(new_x, new_y)

    def ship_heading_change(self, ship):
        """
        changes the heading of the ship in correspondence to button pressed
        :param ship: a ship obj
        """
        if self._screen.is_left_pressed():
            ship.change_direction(LEFT)
        if self._screen.is_right_pressed():
            ship.change_direction(RIGHT)

    def ship_accelerate(self, ship):
        """
        accelerate the ship if up was pressed
        :param ship: a ship obj
        """
        if self._screen.is_up_pressed():
            self.accelerate_object(ship)

    def random_coordinate(self):
        """
        :return: a random coordinate on one axis of the screen
        """
        random_cod = random.randrange(self.screen_min_x, self.screen_max_x + 1)
        return random_cod

    def fire_torpedo(self, ship):
        """
        fires a torpedo from the ship
        :param ship: a ship object
        """
        if self._screen.is_space_pressed():
            if len(self._torpedoes) < 15:
                torpedo = ship.fire_torpedo()
                self.accelerate_object(torpedo)
                self._screen.register_torpedo(torpedo)
                self._torpedoes.append(torpedo)

    def torpedo_remove(self, torpedo):
        self._screen.unregister_torpedo(torpedo)
        self._torpedoes.remove(torpedo)

    def torpedoes_update(self):
        for torpedo in self._torpedoes:
            if torpedo.alive():
                self.move_object(torpedo)
                self._screen.draw_torpedo(torpedo, *torpedo.get_position(),
                                          torpedo.get_heading())
            else:
                self.torpedo_remove(torpedo)

    def asteroid_removal(self):
        # todo-yanir asteroid removal
        pass

    def _game_loop(self):
        '''
        Your code goes here!
        '''
        self._screen.draw_ship(*self._ship.ship_drawing_parameters())
        self.move_object(self._ship)
        self.ship_heading_change(self._ship)
        self.ship_accelerate(self._ship)
        self.fire_torpedo(self._ship)
        self.torpedoes_update()





def main(amnt):
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( int( sys.argv[1] ) )
    else:
        main( DEFAULT_ASTEROIDS_NUM )
