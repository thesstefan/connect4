import pygame
import sys
import math
import time

from config import settings

class PyGameUI:
    """ GUI implementation using pygame """

    def __init__(self):
        """ Constructs the PyGameUI (initializes internal player to color dict) """
        pygame.init()

        self.__screen = pygame.display.set_mode([
            settings["gui"]["WINDOW_HEIGHT"],
            settings["gui"]["WINDOW_WIDTH"]
        ])

        self.__circle_radius = (settings["gui"]["BOARD_WIDTH"] / settings["game"]["BOARD_WIDTH"]) / 2

        self.__player_to_color = { 0: settings["gui"]["EMPTY_COLOR"] }

        for player in range(1, settings["game"]["NUMBER_OF_PLAYERS"] + 1):
            self.__player_to_color[player] = settings["gui"]["PLAYER_{}_COLOR".format(player)]

        self.__current_column_index = None
        self.__current_player = None

    def __get_x_from_column_index(self, column_index):
        """ 
        Returns the x position given by a board column index
        (x of the given column's center)

        :param column_index: the Board column index to be used
        :tparam column_index: nonnegative integer

        :return: x position
        :rtype: nonnegative float
        """
        return (column_index * 2 + 1) * self.__circle_radius

    def __get_y_from_row_index(self, row_index):
        """ 
        Returns the y position given by a board row index 
        (y of the the given row's center)

        :param row_index: the Board row index to be used
        :tparam row_index: nonnegative integer

        :return: y position
        :rtype: nonnegative float
        """
        return (row_index * 2 + 1) * self.__circle_radius

    def __get_center_position(self, row_index, column_index):
        """ 
        Returns the center of the square positions coresponding
        to given row, column indexes

        :param row_index: the Board row index to be used
        :tparam row_index: nonnegative integer

        :param column_index: the Board column index to be used
        :tparam column_index: nonnegative integer

        :return: (x, y) position
        :rtype: tuple of nonnegative floats (length 2)
        """
        return (self.__get_x_from_column_index(column_index), 
                self.__get_y_from_row_index(row_index) + settings["gui"]["DROP_ZONE_HEIGHT"])

    def __draw_piece(self, x_position, y_position, player):
        """ Draws piece coresponding to a given player at the given position """
        pygame.draw.circle(self.__screen, 
                           self.__player_to_color[player],
                           (x_position, y_position),
                           self.__circle_radius - settings["gui"]["DISTANCE_BETWEEN_CIRCLES"])

    def __draw_board_piece(self, row_index, column_index, player):
        """ 
        Draws a piece matching a given player using coresponding
        row, column board indexes
        """
        center_position = self.__get_center_position(row_index, column_index)
        self.__draw_piece(center_position[0], center_position[1], player)

    def __draw_drop_zone(self):
        """ Draws the drop zone """
        pygame.draw.rect(self.__screen, settings["gui"]["DROP_ZONE_COLOR"], 
                        (settings["gui"]["DROP_ZONE_X"],
                         settings["gui"]["DROP_ZONE_Y"],
                         settings["gui"]["DROP_ZONE_WIDTH"],
                         settings["gui"]["DROP_ZONE_HEIGHT"]))

    def __draw_board(self, board):
        """ Draws the board """
        pygame.draw.rect(self.__screen, settings["gui"]["BOARD_COLOR"],
                        (settings["gui"]["BOARD_X"],
                         settings["gui"]["BOARD_Y"],
                         settings["gui"]["BOARD_WIDTH"],
                         settings["gui"]["BOARD_HEIGHT"]))

        for row_index in range(board.height):
            for column_index in range(board.width):
                self.__draw_board_piece(row_index, column_index, board[row_index][column_index])

    def __draw_falling_piece(self, x_position, board, player):
        """ Draws falling piece animation """
        square_size = int(self.__circle_radius + settings["gui"]["DISTANCE_BETWEEN_CIRCLES"])
        y_start = settings["gui"]["BOARD_Y"] + square_size 
        top_occupied_row_index = board.get_top_occupied_row_index(self.__current_column_index) 
        y_stop = int(top_occupied_row_index + 1) * square_size * 2

        y_position = y_start
        piece_fall_speed = settings["gui"]["PIECE_FALL_SPEED"]

        while y_position < y_stop:
            self.__draw_board(board)
            self.__draw_board_piece(top_occupied_row_index, self.__current_column_index, 0)

            self.__draw_piece(x_position, y_position, player)

            pygame.display.flip()
            clock = pygame.time.Clock()
            clock.tick(settings["gui"]["FPS"])

            y_position += piece_fall_speed

        self.__draw_board(board)
        pygame.display.flip()
        time.sleep(0.1)

    def draw(self, board):
        """ 
        Draws the main falling piece animation and the board
        (main view)

        :param board: the Board to be used
        :tparam board: Board
        """
        if self.__current_column_index is not None and self.__current_player is not None:
            x_position = self.__get_x_from_column_index(self.__current_column_index)
            self.__draw_falling_piece(x_position, board, self.__current_player)

        self.__draw_board(board)

        pygame.display.flip()

    def make_move(self, column_choice, player):
        """ 
        Stores current player and column choice for future use 
        (falling piece animation)

        :param column_choice: the chosen column
        :tparam column_choice: nonnegative integer

        :param player: the player that makes the move
        :tparam player: player id value
        """
        self.__draw_drop_zone()
        pygame.display.flip()

        self.__current_column_index = column_choice
        self.__current_player = player

    def get_move(self, current_player, valid_moves):
        """ 
        Returns the column chosen by the player

        :param current_player: the player that is chosing the column
        :tparam current_player player id value

        :param valid_moves: the current valid drop column indexes
        :tparam valid_moves: list of nonnegative integers

        :return: column chosen by player
        :rtype: nonnegative integer
        """
        column_choice = None

        while column_choice not in valid_moves:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    x_position = event.pos[0]

                    self.__draw_drop_zone()
                    self.__draw_piece(x_position, self.__circle_radius, current_player)
                    pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__draw_drop_zone()
                    pygame.display.flip()

                    x_position = event.pos[0]

                    self.__current_column_index = int(math.floor(x_position / (self.__circle_radius * 2)))
                    self.__current_player = current_player

                    if self.__current_column_index not in valid_moves:
                        continue 

                    return self.__current_column_index

    def display_winner(self, winner):
        """ 
        Displays the winner player

        :param winner: the winner player
        :tparam winner: player value id
        """
        self.__screen.fill(settings["gui"]["WINNER_BACKGROUND_COLOR"])

        font = pygame.font.SysFont(settings["gui"]["FONT_NAME"],
                                   settings["gui"]["FONT_SIZE"])

        text = font.render("{} won!".format(settings["game"]["PLAYER_{}_NAME".format(winner)]),
                           True, 
                           self.__player_to_color[winner],
                           settings["gui"]["WINNER_BACKGROUND_COLOR"])

        text_rect = text.get_rect()
        text_rect.center = (settings["gui"]["WINDOW_WIDTH"] // 2, settings["gui"]["WINDOW_HEIGHT"] // 2)

        self.__screen.blit(text, text_rect)

        pygame.display.flip()
        time.sleep(1)
