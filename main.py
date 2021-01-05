from tkinter import *

import numpy as np

size_of_board = 600
number_of_dots = 6
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
dot_color_p1 = '#FF3333'
dot_color_p2 = '#33B3FF'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots
distance_between_dots = size_of_board / number_of_dots


class BoxesGame:
    def __init__(self):
        self.window = Tk()
        self.window.title('Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.player1_turn = True
        self.player2_turn = False
        self.play_again()
        self.window.bind('<Key>', self.on_key_click)

    def on_key_click(self, event):
        if event.char != event.keysym and len(event.char) != 1:
            if self.player1_turn is True:
                result_position_info = self.update_position(event.keysym, self.player1_position, True)
                if result_position_info[0]:
                    self.player1_position = (result_position_info[1], result_position_info[2])
                    self.player1_turn = False
            else:
                result_position_info = self.update_position(event.keysym, self.player2_position, False)
                if result_position_info[0]:
                    self.player2_position = (result_position_info[1], result_position_info[2])
                    self.player1_turn = True

        print(self.board_status)

    def update_position(self, pressed_key, player_position, is_player_1):
        new_player_position_x = -1
        new_player_position_y = -1

        current_player_indicator = 1 if is_player_1 is True else 2
        enemy_player_indicator = 2 if is_player_1 is True else 1
        is_valid = False
        if pressed_key == "Up":
            new_player_position_x = player_position[0] - 1
            new_player_position_y = player_position[1]
            if new_player_position_x >= 0 and self.board_status[new_player_position_x][new_player_position_y] != enemy_player_indicator:
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator
                is_valid = True
        elif pressed_key == "Right":
            new_player_position_x = player_position[0]
            new_player_position_y = player_position[1] + 1
            if new_player_position_y < number_of_dots and self.board_status[new_player_position_x][new_player_position_y] != enemy_player_indicator:
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator
                is_valid = True
        elif pressed_key == "Down":
            new_player_position_x = player_position[0] + 1
            new_player_position_y = player_position[1]
            if new_player_position_x < number_of_dots and self.board_status[new_player_position_x][new_player_position_y] != enemy_player_indicator:
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator
                is_valid = True
        elif pressed_key == "Left":
            new_player_position_x = player_position[0]
            new_player_position_y = player_position[1] - 1
            if new_player_position_y >= 0 and self.board_status[new_player_position_x][new_player_position_y] != enemy_player_indicator:
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator
                is_valid = True
        return is_valid, new_player_position_x, new_player_position_y

    def play_again(self):
        self.player1_turn = True
        self.player2_turn = False

        self.player1_position = (0, 0)
        self.player2_position = (number_of_dots - 1, number_of_dots - 1)

        self.board_status = np.zeros(shape=(number_of_dots, number_of_dots))

        self.board_status[0][0] = 1
        self.board_status[number_of_dots - 1][number_of_dots - 1] = 2

        self.refresh_board()

    def mainloop(self):
        self.window.mainloop()

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i * distance_between_dots + distance_between_dots / 2
            self.canvas.create_line(x, distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i * distance_between_dots + distance_between_dots / 2
                end_x = j * distance_between_dots + distance_between_dots / 2

                color = dot_color
                if i == 0 and j == 0:
                    color = dot_color_p1
                elif i == number_of_dots - 1 and j == number_of_dots - 1:
                    color = dot_color_p2

                self.canvas.create_oval(start_x - dot_width / 2, end_x - dot_width / 2, start_x + dot_width / 2,
                                        end_x + dot_width / 2, fill=color,
                                        outline=color)

game_instance = BoxesGame()
game_instance.mainloop()
