#############################################################
# FILE: asteroids_main.py
# EXERCISE: intro2cs ex9 2016-2017
# DESCRIPTION: Game manages for the asteroids game
#############################################################

import random
import sys
from math import sin, cos, radians, sqrt, pow
from screen import Screen
from ship import Ship
from asteriod import Asteriod
from torpedo import Torpedo


DEFAULT_ASTEROIDS_NUM = 5
RIGHT = -7
LEFT = 7
SHIT_HIT_TITLE = "You've been hit"
SHIP_HIT_MSG = "Ship has been hit \n ლ(ಠ益ಠლ)"
OVER = 'GAME OVER'
OUT_OF_LIFE = 'YOU DIED'
QUIT = 'Rage quit? \n (ノಠ益ಠ)ノ彡┻━┻'
WIN = 'GZ , you won!!!!\n ಠ‿↼ '
SMALL_POINTS = 100
MEDIUM_POINTS = 50
LARGE_POINTS = 20
SIZE_LARGE = 3
SIZE_MEDIUM = 2
SIZE_SMALL = 1
AXIS_X = 0
AXIS_Y = 1

class GameRunner:

    def __init__(self, asteroids_amnt):
        # the next 5 lines define the game screen
        self._screen = Screen()
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        # making the ship
        self._ship = Ship(self.random_coordinate(), self.random_coordinate())
        # the astro list will store the data about the asteroids in the game
        self.__astro_list = []
        # making the asteroids
        for i in range(asteroids_amnt):
            astro = self.make_astro()
            self.add_astro(astro)
        self._torpedoes = []    # will store the data about the torpedoes
        self.__score = 0

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
        # the net two lines calculates the new speed by the formula
        new_x_speed = current_x_speed +\
                      (obj.ACCEL_FACTOR * cos(radians(obj.get_heading())))
        new_y_speed = current_y_speed + \
                      (obj.ACCEL_FACTOR * sin(radians(obj.get_heading())))
        obj.set_speed(new_x_speed, new_y_speed)

    def update_score(self, asteroid):
        """
        Updating the score value  according to the asteroid size changing the
        display on the screen
        """
        value = 0
        size = asteroid.get_size()  # getting the hit asteroid size
        if size == SIZE_LARGE:
            value = LARGE_POINTS
        elif size == SIZE_MEDIUM:
            value = MEDIUM_POINTS
        elif size == SIZE_SMALL:
            value = SMALL_POINTS
        self.__score += value   # updating the score
        self._screen.set_score(self.__score)    # updating screen display

    def move_object(self, obj):
        """
        moves an object withing the game.
        function assumes object has get_position function that returns a
        tuple of (x,y) coordinates and get_speed with the same return values.
        also assume object has a position setter
        """
        old_x, old_y = obj.get_position()
        x_speed, y_speed = obj.get_speed()
        # making the new place by the formula
        delta_axis = self.screen_max_x - self.screen_min_x
        new_x = (x_speed + old_x - self.screen_min_x) % delta_axis\
                + self.screen_min_x
        new_y = (y_speed + old_y - self.screen_min_y) % delta_axis\
                + self.screen_min_y
        obj.set_position(new_x, new_y)  # setting the new place

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
        """
        removes a torpedo from the game
        :param torpedo: a torpedo object
        """
        self._screen.unregister_torpedo(torpedo)
        self._torpedoes.remove(torpedo)

    def torpedoes_update(self):
        """
        updates the state of all torpedoes currently in play.
        including removing them if they are dead
        :return:
        """
        for torpedo in self._torpedoes:
            if torpedo.alive():
                self.move_object(torpedo)
                self._screen.draw_torpedo(torpedo, *torpedo.get_position(),
                                          torpedo.get_heading())
            else:
                self.torpedo_remove(torpedo)

    def make_astro(self):
        """
        makes an asteroid not at the ship position
        :return:
        """
        ast = Asteriod(self.random_coordinate(), self.random_coordinate())
        while ast.is_in_position(self._ship.get_position()):
            ast.set_position(self.random_coordinate(),
                             self.random_coordinate())
        return ast

    def add_astro(self, asteroid):
        """
        gets an asteroid and adds it to the asteroids list and register it
        :param asteroid:
        """
        self.__astro_list.append(asteroid)
        self._screen.register_asteroid(asteroid, asteroid.get_size())

    def asteroid_removal(self, asteroid):
        """
        gets an asteroid, removes it from the list and unregister it
        :param asteroid:
        :return:
        """
        self.__astro_list.remove(asteroid)
        self._screen.unregister_asteroid(asteroid)

    def draw_asteroids(self):
        """
        Draws the asteroids on the screen
        """
        for ast in self.__astro_list:
            self._screen.draw_asteroid(ast, *ast.get_position())

    def move_asteroids(self):
        """
        Makes all the asteroids to move
        """
        for ast in self.__astro_list:
            self.move_object(ast)

    def ship_collision(self, ship, asteroid):
        """
        actions to do in case the asteroid collision was with the ship
        :param ship:
        :param asteroid:
        :return:
        """
        # Print message about the collision
        self._screen.show_message(SHIT_HIT_TITLE, SHIP_HIT_MSG)
        self._screen.remove_life()  # updating the life status on the screen
        if ship.lose_a_life():  # takes down one life
            # if the ship is still alive - remove asteroid
            self.asteroid_removal(asteroid)
        else:
            # if no more life left, end the game
            self.end_game(OUT_OF_LIFE)

    def asteroid_torpedo_hit(self, asteroid, torpedo):
        """
        Changing the asteroid size and speed according to the game rules
        :param asteroid:
        :param torpedo:
        """
        old_ast_size = asteroid.get_size()  # size before the hit
        ast_speed = asteroid.get_speed()
        ast_pos = asteroid.get_position()
        # norm speed for the formula, looks better
        norm_speed = sqrt(pow(ast_speed[AXIS_X],2) + pow(ast_speed[AXIS_Y],2))
        torpedo_speed = torpedo.get_speed()
        if old_ast_size == SIZE_SMALL:
            # if the asteroid is the smallest, remove it.
            self.asteroid_removal(asteroid)
            return
        else:
            new_ast_size = old_ast_size - 1
            new_speed_x_1 = (torpedo_speed[AXIS_X] + ast_speed[AXIS_X]) /\
                            norm_speed
            new_speed_y_1 = (torpedo_speed[AXIS_Y] + ast_speed[AXIS_Y]) / \
                            norm_speed
            # other asteroid speed is filliped
            new_speed_x_2 = new_speed_x_1 * (-1)
            new_speed_y_2 = new_speed_y_1 * (-1)
        # the next lines makes two new asteroids and adds them by the games
        # rules and removes the old asteroid
        new_asteroid_1 = Asteriod(*ast_pos, new_ast_size)
        new_asteroid_2 = Asteriod(*ast_pos, new_ast_size)
        new_asteroid_1.set_speed(new_speed_x_1, new_speed_y_1)
        new_asteroid_2.set_speed(new_speed_x_2, new_speed_y_2)
        self.add_astro(new_asteroid_1)
        self.add_astro(new_asteroid_2)
        self.asteroid_removal(asteroid)

    def torpedo_collision(self, torpedo, asteroid):
        """
        function that is called upon when torpedo-asteroid collision
        is detected
        :param torpedo: hitting torpedo object
        :param asteroid: asteroid hitted
        """
        self.update_score(asteroid)
        self.asteroid_torpedo_hit(asteroid,torpedo)

    def check_collisions(self, ship, asteroid_list, torpedo_list):
        """
        A function that check collisions between asteroid and other objects
        and calls the appropriate functions for thos collisions
        :param ship: ship object
        :param asteroid_list: a list of asteroid objects
        :param torpedo_list: a list of torpedo objects
        """
        for asteroid in asteroid_list:
            if asteroid.has_intersection(ship):
                self.ship_collision(ship, asteroid)
                continue
            else:
                for torpedo in torpedo_list:
                    if asteroid.has_intersection(torpedo):
                        self.torpedo_collision(torpedo, asteroid)
                        self.torpedo_remove(torpedo)

    def end_game(self, message):
        """
        A functions that put an end to the game with a message
        """
        self._screen.show_message(OVER, message)
        self._screen.end_game()
        sys.exit()

    def _game_loop(self):
        '''
        Your code goes here!
        '''
        if self._screen.should_end():
            self.end_game(QUIT)
        self._screen.draw_ship(*self._ship.ship_drawing_parameters())
        self.draw_asteroids()
        self.move_object(self._ship)
        self.move_asteroids()
        self.ship_heading_change(self._ship)
        self.ship_accelerate(self._ship)
        self.fire_torpedo(self._ship)
        self.torpedoes_update()
        self.check_collisions(self._ship, self.__astro_list, self._torpedoes)
        if len(self.__astro_list) == 0:
            self.end_game(WIN)



def main(amnt):
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( int( sys.argv[1] ) )
    else:
        main( DEFAULT_ASTEROIDS_NUM )
