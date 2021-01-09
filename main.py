from tkinter import *

import numpy as np
import numpy.linalg as deter

size_of_board = 700
number_of_dots = 6
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#FFFFFF'
dot_color_p1 = '#FF3333'
dot_color_p2 = '#33B3FF'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'

dot_width = 0.25 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots
distance_between_dots = size_of_board / number_of_dots
line_player_1_color = '#ff746c'
line_player_2_color = '#72d5ff'
player_1_value = 1
player_2_value = 5


class BoxesGame:
    def __init__(self):
        self.window = Tk()
        self.window.title('Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.player1_turn = True
        self.score_items = []
        self.play_again()
        self.window.bind('<Key>', self.on_key_click)
        self.player_1_score = 0
        self.player_2_score = 0

    def on_key_click(self, event):
        if event.char != event.keysym and len(event.char) != 1:
            if self.player1_turn is True:
                result_position_info = self.update_position(event.keysym, self.player1_position, True)
                if result_position_info[0]:
                    new_position = (result_position_info[1], result_position_info[2])
                    self.draw_board(self.player1_position, new_position, dot_color_p1, player1_color_light,
                                    self.player2_position, dot_color_p2, player2_color_light)
                    self.player1_position = new_position
                    self.player1_turn = False

                self.player_1_score = self.square_count(player_1_value, self.board_status)

            else:
                result_position_info = self.update_position(event.keysym, self.player2_position, False)
                if result_position_info[0]:
                    new_position = (result_position_info[1], result_position_info[2])
                    self.draw_board(self.player2_position, new_position, dot_color_p2, player2_color_light,
                                    self.player1_position, dot_color_p1, player1_color_light)
                    self.player2_position = new_position
                    self.player1_turn = True

                self.player_2_score = self.square_count(player_2_value, self.board_status)
            self.create_score_board(self.player_1_score, self.player_2_score)

    def draw_board(self, old_position, current_position, color_1, color_2, opposite_player_position,
                   opposite_player_color_1, opposite_player_color_2):
        self.check_edges_to_draw(current_position)
        self.draw_player_position(old_position, color_1, color_1, 2)
        self.draw_player_position(current_position, color_1, color_2, 2)
        self.draw_player_position(opposite_player_position, opposite_player_color_1, opposite_player_color_2, 5)

    def draw_player_position(self, current_position, color, color_2, width):
        j = current_position[0]
        i = current_position[1]
        start_x = i * distance_between_dots + distance_between_dots / 2
        end_x = j * distance_between_dots + distance_between_dots / 2

        self.canvas.delete(self.dots[j][i])
        self.dots[j][i] = self.canvas.create_oval(start_x - dot_width / 2, end_x - dot_width / 2, start_x + dot_width / 2,
                                                  end_x + dot_width / 2, fill=color,
                                                  outline=color_2, width=width)

    def check_edges_to_draw(self, current_position):
        x = current_position[0]
        y = current_position[1]

        if self.player1_turn is True:
            value_to_check = player_1_value
        else:
            value_to_check = player_2_value

        if x - 1 >= 0 and self.board_status[x - 1][y] == value_to_check:  # check upper point
            self.make_edge(current_position, ((x - 1), y))
        if y - 1 >= 0 and self.board_status[x][y - 1] == value_to_check:  # check right point
            self.make_edge(current_position, (x, (y - 1)))
        if x + 1 < number_of_dots and self.board_status[x + 1][y] == value_to_check:  # check lower point
            self.make_edge(current_position, ((x + 1), y))
        if y + 1 < number_of_dots and self.board_status[x][y + 1] == value_to_check:  # check right point
            self.make_edge(current_position, (x, (y + 1)))

    def make_edge(self, start, end):
        if self.player1_turn:
            color = line_player_1_color
        else:
            color = line_player_2_color
        s_point_x = start[1] * distance_between_dots + distance_between_dots / 2
        s_point_y = start[0] * distance_between_dots + distance_between_dots / 2

        e_point_x = end[1] * distance_between_dots + distance_between_dots / 2
        e_point_y = end[0] * distance_between_dots + distance_between_dots / 2
        self.canvas.create_line(s_point_x, s_point_y, e_point_x, e_point_y, fill=color, width=edge_width)

    def update_position(self, pressed_key, player_position, is_player_1):
        new_player_position_x = -1
        new_player_position_y = -1

        current_player_indicator = player_1_value if is_player_1 is True else player_2_value
        enemy_player_indicator = player_2_value if is_player_1 is True else player_1_value
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

        self.board_status[0][0] = player_1_value
        self.board_status[number_of_dots - 1][number_of_dots - 1] = player_2_value

        self.create_score_board(str(0), str(0))

        self.refresh_board()

    def create_score_board(self, player_1_score, player_2_score):
        for item in self.score_items:
            self.canvas.delete(item)
        self.score_items.append(self.canvas.create_text(150, 15, fill=dot_color_p1, font="Times 20 bold",
                                                        text="Player 1:"))
        self.score_items.append(self.canvas.create_text(220, 15, fill="black", font="Times 20 bold",
                                                        text=player_1_score))
        self.score_items.append(self.canvas.create_text(500, 15, fill=dot_color_p2, font="Times 20 bold",
                                                        text="Player 2:"))
        self.score_items.append(self.canvas.create_text(570, 15, fill="black", font="Times 20 bold",
                                                        text=player_2_score))

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

        self.dots = []
        for j in range(number_of_dots):
            temp = []
            for i in range(number_of_dots):
                start_x = i * distance_between_dots + distance_between_dots / 2
                end_x = j * distance_between_dots + distance_between_dots / 2

                color = dot_color
                outline_color = dot_color
                outline_width = 1
                if i == 0 and j == 0:
                    color = dot_color_p1
                    outline_color = player1_color_light
                    outline_width = 5
                elif i == number_of_dots - 1 and j == number_of_dots - 1:
                    color = dot_color_p2
                    outline_color = player2_color_light
                    outline_width = 1
                oval = self.canvas.create_oval(start_x - dot_width / 2, end_x - dot_width / 2, start_x + dot_width / 2,
                                               end_x + dot_width / 2, fill=color, outline=outline_color, width=outline_width)
                temp.append(oval)
            self.dots.append(temp)

    def square_count(self, val, board_status):
        turn = val
        p1_count = 0
        p2_count = 0
        bigger_matrix = 6
        smaller_matrix = 2
        p = bigger_matrix - smaller_matrix + 1
        x = np.arange(p).repeat(smaller_matrix)
        y = np.tile(np.arange(smaller_matrix), p) + x

        b = board_status[np.newaxis].repeat(p, axis=0)
        c = b[x, y]

        d = c.reshape(p, smaller_matrix, bigger_matrix)

        e = d[:, np.newaxis].repeat(p, axis=1)
        f = e[:, x, :, y]
        g = f.reshape(p, smaller_matrix, p, smaller_matrix)
        h = g.transpose(2, 0, 3, 1)

        for i in range(0, p):
            for j in range(0, p):
                if deter.det(h[i, j]) == 0 and np.sum(h[i, j]) == turn * 4:
                    if turn == 1:
                        p1_count += 1
                    else:
                        p2_count += 1

        if val == 1:
            return p1_count
        else:
            return p2_count


game_instance = BoxesGame()
game_instance.mainloop()
