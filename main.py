board_size = 5

import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb

import numpy as np
import numpy.linalg as deter
from pymongo import MongoClient
import random

uri = "mongodb+srv://elif:elif@cluster0.pj6ji.mongodb.net/test"
my_db_cli = MongoClient(uri)
db = my_db_cli.SquaresGame
my_scores = db.scores
player_1_indicator = 1
player_2_indicator = 5


class Minimax:
    def __init__(self, board_size_as_prm):
        self.board_size = board_size_as_prm
        self.number_of_dots = board_size
        self.size_of_board = 700
        self.dot_color = '#FFFFFF'
        self.dot_color_p1 = '#FF3333'
        self.dot_color_p2 = '#33B3FF'
        self.player1_color_light = '#67B0CF'
        self.player2_color_light = '#EE7E77'
        self.dot_width = 0.25 * self.size_of_board / self.number_of_dots
        self.edge_width = 0.1 * self.size_of_board / self.number_of_dots
        self.distance_between_dots = self.size_of_board / self.number_of_dots
        self.line_player_1_color = '#ff746c'
        self.line_player_2_color = '#72d5ff'
        self.player_1_value = 1
        self.player_2_value = 5
        self.empty_indicator = 0

        self.board_status = np.zeros(shape=(self.number_of_dots, self.number_of_dots))

        self.give_random_position_for_player()
        self.player1_position = self.p1_starting_pos
        self.player2_position = self.p2_starting_pos
        self.window = Tk()
        self.window.title('Boxes')
        self.canvas = Canvas(self.window, width=self.size_of_board + 200, height=self.size_of_board)
        self.canvas.pack()
        self.player1_turn = True
        self.score_items = []
        self.lines = []
        self.items_dot = []
        self.game_end_text = []
        self.player_1_score = 0
        self.player_2_score = 0
        self.canvas.bind_all('<Key>', self.on_key_click)

        self.is_in_start_page = True

    def give_random_position_for_player(self):
        x_1 = random.randint(0, self.board_size-1)
        y_1 = random.randint(0, self.board_size-1)

        x_2 = random.randint(0, self.board_size-1)
        y_2 = random.randint(0, self.board_size-1)

        while x_1 == x_2 and y_1 == y_2:
            x_2 = random.randint(0, self.board_size-1)
            y_2 = random.randint(0, self.board_size-1)

        self.p1_starting_pos = (x_1, y_1)
        self.p2_starting_pos = (x_2, y_2)

    def square_count(self, val, board_status):
        turn = val
        p1_count = 0
        p2_count = 0
        bigger_matrix = self.board_size
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

    def is_end(self, possible_positions):
        if np.count_nonzero(self.board_status == 0) == 0 or len(possible_positions) == 0:
            p_1_count = self.square_count(player_1_indicator, self.board_status)
            p_2_count = self.square_count(player_2_indicator, self.board_status)

            if p_1_count > p_2_count:
                return player_1_indicator
            elif p_1_count < p_2_count:
                return player_2_indicator
            else:
                return 0
        return None

    def get_possible_positions(self, current_player_position):
        possible_positions = []

        current_player_position_x = current_player_position[0]
        current_player_position_y = current_player_position[1]
        if current_player_position_x - 1 >= 0 and self.board_status[current_player_position_x - 1][current_player_position_y] == 0:
            possible_positions.append((current_player_position_x - 1, current_player_position_y))

        if current_player_position_x + 1 < self.board_size and self.board_status[current_player_position_x + 1][current_player_position_y] == 0:
            possible_positions.append((current_player_position_x + 1, current_player_position_y))

        if current_player_position_y - 1 >= 0 and self.board_status[current_player_position_x][current_player_position_y - 1] == 0:
            possible_positions.append((current_player_position_x, current_player_position_y - 1))

        if current_player_position_y + 1 < self.board_size and self.board_status[current_player_position_x][current_player_position_y + 1] == 0:
            possible_positions.append((current_player_position_x, current_player_position_y + 1))

        filtered_possible_position = []
        for possible_position in possible_positions:
            pos_x = possible_position[0]
            pos_y = possible_position[1]
            #   +
            # + + +
            #   +
            if pos_x - 1 >= 0 and pos_x + 1 < self.board_size and pos_y + 1 < self.board_size and pos_y - 1 >= 0:
                if self.board_status[pos_x - 1][pos_y] != 0 and self.board_status[pos_x + 1][pos_y] != 0 and self.board_status[pos_x][pos_y + 1] != 0 and \
                        self.board_status[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            # + +
            # +
            #
            elif pos_x + 1 < self.board_size and pos_y + 1 < self.board_size:
                if self.board_status[pos_x + 1][pos_y] != 0 and self.board_status[pos_x][pos_y + 1] != 0:
                    filtered_possible_position.append(possible_position)
            #   + +
            #     +
            #
            elif pos_x - 1 >= 0 and pos_y + 1 < self.board_size:
                if self.board_status[pos_x - 1][pos_y] != 0 and self.board_status[pos_x][pos_y + 1] != 0:
                    filtered_possible_position.append(possible_position)
            #
            # +
            # + +
            elif pos_x + 1 < self.board_size and pos_y - 1 >= 0:
                if self.board_status[pos_x + 1][pos_y] != 0 and self.board_status[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            #
            #     +
            #   + +
            elif pos_x - 1 >= 0 and pos_y - 1 >= 0:
                if self.board_status[pos_x - 1][pos_y] != 0 and self.board_status[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            #  +
            #  + +
            #  +
            elif pos_x + 1 < self.board_size and pos_y + 1 < self.board_size and pos_y - 1 >= 0:
                if self.board_status[pos_x + 1][pos_y] != 0 and self.board_status[pos_x][pos_y + 1] != 0 and self.board_status[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            #  + + +
            #    +
            #
            elif pos_x - 1 >= 0 and pos_x + 1 < self.board_size and pos_y + 1 < self.board_size:
                if self.board_status[pos_x - 1][pos_y] != 0 and self.board_status[pos_x + 1][pos_y] != 0 and self.board_status[pos_x][pos_y + 1] != 0:
                    filtered_possible_position.append(possible_position)
            #     +
            #   + +
            #     +
            elif pos_x - 1 >= 0 and pos_y + 1 < self.board_size and pos_y - 1 >= 0:
                if self.board_status[pos_x - 1][pos_y] != 0 and self.board_status[pos_x][pos_y + 1] != 0 and self.board_status[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            #
            #    +
            #  + + +
            elif pos_x - 1 >= 0 and pos_x + 1 < self.board_size and pos_y - 1 >= 0:
                if self.board_status[pos_x - 1][pos_y] != 0 and self.board_status[pos_x][pos_y + 1] != 0 and self.board_status[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)

        f_result = set(possible_positions) - set(filtered_possible_position)
        if len(f_result) > 0:
            possible_positions = list(f_result)
        return possible_positions

    def max(self, current_p1_position, current_p2_position, alpha, beta):
        maxv = -1 * (self.board_size * self.board_size)

        px = None
        py = None

        possible_positions = self.get_possible_positions(current_p1_position)
        result = self.is_end(possible_positions)

        if result is not None:
            if len(self.get_possible_positions(current_p2_position)) > 0:
                (m, min_i, min_j) = self.min(current_p1_position, current_p2_position, alpha, beta)
                i = current_p1_position[0]
                j = current_p1_position[1]
                # Fixing the maxv value if needed
                if m > maxv:
                    maxv = m
                    px = i
                    py = j
                return maxv, px, py
            p_1_count = self.square_count(player_1_indicator, self.board_status)
            p_2_count = self.square_count(player_2_indicator, self.board_status)

            if result == player_2_indicator:
                return (-1 * p_2_count, current_p1_position[0], current_p1_position[1])
            elif result == player_1_indicator:
                return (p_1_count, current_p1_position[0], current_p1_position[1])
            elif result == 0:
                return (0, current_p1_position[0], current_p1_position[1])

        for position in possible_positions:
            i = position[0]
            j = position[1]
            self.board_status[i][j] = player_1_indicator

            (m, min_i, min_j) = self.min((i, j), current_p2_position, alpha, beta)
            # Fixing the maxv value if needed
            if m > maxv:
                maxv = m
                px = i
                py = j
            # Setting back the field to empty
            self.board_status[i][j] = 0

            if maxv >= beta:
                return maxv, px, py

            if maxv > alpha:
                alpha = maxv
        return maxv, px, py

    # Player 'player 2' is min
    def min(self, current_p1_position, current_p2_position, alpha, beta):
        # We're initially setting it to 2 as worse than the worst case:
        minv = self.board_size * self.board_size

        qx = None
        qy = None
        possible_positions = self.get_possible_positions(current_p2_position)
        result = self.is_end(possible_positions)

        if result is not None:
            if len(self.get_possible_positions(current_p1_position)) > 0:
                (m, min_i, min_j) = self.max(current_p1_position, current_p2_position, alpha, beta)
                i = current_p1_position[0]
                j = current_p1_position[1]
                if m < minv:
                    minv = m
                    qx = i
                    qy = j
                return minv, self.player2_position[0], self.player2_position[1]

            p_1_count = self.square_count(player_1_indicator, self.board_status)
            p_2_count = self.square_count(player_2_indicator, self.board_status)

            if result == player_2_indicator:
                return (-1 * p_2_count, current_p2_position[0], current_p2_position[1])
            elif result == player_1_indicator:
                return (p_1_count, current_p2_position[0], current_p2_position[1])
            elif result == 0:
                return (0, current_p2_position[0], current_p2_position[1])
        for position in possible_positions:
            i = position[0]
            j = position[1]
            self.board_status[i][j] = player_2_indicator

            (m, max_i, max_j) = self.max(current_p1_position, (i, j), alpha, beta)
            if m < minv:
                minv = m
                qx = i
                qy = j
            self.board_status[i][j] = 0

            if minv <= alpha:
                return minv, qx, qy

            if minv < beta:
                beta = minv
        return minv, qx, qy

    def on_key_click(self, event):
        if self.player1_turn is True:
            if event.char != event.keysym and len(event.char) != 1:
                result_position_info = self.update_position(event.keysym, self.player1_position, True)
                if result_position_info[0]:
                    new_position = (result_position_info[1], result_position_info[2])
                    self.draw_board(self.player1_position, new_position, self.dot_color_p1, self.player1_color_light,
                                    self.player2_position, self.dot_color_p2, self.player2_color_light)
                    self.player1_position = new_position
                    self.player1_turn = False
                    self.play()

                self.player_1_score = self.square_count(self.player_1_value, self.board_status)
                self.create_score_board(self.player_1_score, self.player_2_score)
        if self.is_over():
            self.create_game_end_panel(self.player_1_score, self.player_2_score)
            self.callback()

    def draw_board(self, old_position, current_position, color_1, color_2, opposite_player_position,
                   opposite_player_color_1, opposite_player_color_2):
        self.check_edges_to_draw(current_position)
        self.draw_player_position(old_position, color_1, color_1, 2)
        self.draw_player_position(current_position, color_1, color_2, 2)
        self.draw_player_position(opposite_player_position, opposite_player_color_1, opposite_player_color_2, 5)

    def draw_player_position(self, current_position, color, color_2, width):
        j = current_position[0]
        i = current_position[1]
        start_x = i * self.distance_between_dots + self.distance_between_dots / 2
        end_x = j * self.distance_between_dots + self.distance_between_dots / 2

        self.canvas.delete(self.dots[j][i])
        self.dots[j][i] = self.canvas.create_oval(start_x - self.dot_width / 2, end_x - self.dot_width / 2,
                                                  start_x + self.dot_width / 2,
                                                  end_x + self.dot_width / 2, fill=color,
                                                  outline=color_2, width=width)
        self.items_dot.append(self.dots[j][i])

    def check_edges_to_draw(self, current_position):
        x = current_position[0]
        y = current_position[1]

        if self.player1_turn is True:
            value_to_check = self.player_1_value
        else:
            value_to_check = self.player_2_value

        if x - 1 >= 0 and self.board_status[x - 1][y] == value_to_check:  # check upper point
            self.make_edge(current_position, ((x - 1), y))
        if y - 1 >= 0 and self.board_status[x][y - 1] == value_to_check:  # check right point
            self.make_edge(current_position, (x, (y - 1)))
        if x + 1 < self.number_of_dots and self.board_status[x + 1][y] == value_to_check:  # check lower point
            self.make_edge(current_position, ((x + 1), y))
        if y + 1 < self.number_of_dots and self.board_status[x][y + 1] == value_to_check:  # check right point
            self.make_edge(current_position, (x, (y + 1)))

    def make_edge(self, start, end):
        if self.player1_turn:
            color = self.line_player_1_color
        else:
            color = self.line_player_2_color
        s_point_x = start[1] * self.distance_between_dots + self.distance_between_dots / 2
        s_point_y = start[0] * self.distance_between_dots + self.distance_between_dots / 2

        e_point_x = end[1] * self.distance_between_dots + self.distance_between_dots / 2
        e_point_y = end[0] * self.distance_between_dots + self.distance_between_dots / 2
        self.lines.append(
            self.canvas.create_line(s_point_x, s_point_y, e_point_x, e_point_y, fill=color, width=self.edge_width))

    def update_position(self, pressed_key, player_position, is_player_1):
        new_player_position_x = -1
        new_player_position_y = -1

        current_player_indicator = self.player_1_value if is_player_1 is True else self.player_2_value
        is_valid = False
        if pressed_key == "Up":
            new_player_position_x = player_position[0] - 1
            new_player_position_y = player_position[1]
            if new_player_position_x >= 0 and self.board_status[new_player_position_x][new_player_position_y] == self.empty_indicator:
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator
                is_valid = True
        elif pressed_key == "Right":
            new_player_position_x = player_position[0]
            new_player_position_y = player_position[1] + 1
            if new_player_position_y < self.number_of_dots and self.board_status[new_player_position_x][new_player_position_y] == self.empty_indicator:
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator
                is_valid = True
        elif pressed_key == "Down":
            new_player_position_x = player_position[0] + 1
            new_player_position_y = player_position[1]
            if new_player_position_x < self.number_of_dots and self.board_status[new_player_position_x][new_player_position_y] == self.empty_indicator:
                is_valid = True
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator

        elif pressed_key == "Left":
            new_player_position_x = player_position[0]
            new_player_position_y = player_position[1] - 1
            if new_player_position_y >= 0 and self.board_status[new_player_position_x][new_player_position_y] == self.empty_indicator:
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator
                is_valid = True
        return is_valid, new_player_position_x, new_player_position_y

    def play_again(self):
        self.player1_turn = True
        self.board_status = np.zeros(shape=(self.number_of_dots, self.number_of_dots))
        self.give_random_position_for_player()

        self.player2_position = self.p2_starting_pos
        self.player1_position = self.p1_starting_pos
        self.board_status[self.p1_starting_pos[0]][self.p1_starting_pos[1]] = self.player_1_value
        self.board_status[self.p2_starting_pos[0]][self.p2_starting_pos[1]] = self.player_2_value
        self.create_score_board(str(0), str(0))

        self.refresh_board()

    def create_score_board(self, player_1_score, player_2_score):
        for item in self.score_items:
            self.canvas.delete(item)
        self.score_items.append(self.canvas.create_text(750, 60, fill=self.dot_color_p1, font="Times 20 bold",
                                                        text= self.user_name + ":"))
        self.score_items.append(self.canvas.create_text(820, 60, fill="black", font="Times 20 bold",
                                                        text=player_1_score))
        self.score_items.append(self.canvas.create_text(750, 100, fill=self.dot_color_p2, font="Times 20 bold",
                                                        text="AI:"))
        self.score_items.append(self.canvas.create_text(820, 100, fill="black", font="Times 20 bold",
                                                        text=player_2_score))

    def create_game_end_panel(self, player_1_score, player_2_score):
        text = ""
        if player_2_score < player_1_score:
            text = "You \n Win ! "
            my_scores.insert_one({"user_name": self.user_name, "score": player_1_score, "status": "win"})

        elif player_1_score < player_2_score:
            text = "AI \n  Wins !"
            my_scores.insert_one({"user_name": self.user_name, "score": player_1_score, "status": "lose"})

        elif player_1_score == player_2_score:
            text = "  It is \na TIE !"
            my_scores.insert_one({"user_name": self.user_name, "score": player_1_score, "status": "tie"})

        self.game_end_text.append(self.canvas.create_text(700, 220, anchor=W, fill="black", font="Times 35 bold",
                                                          text=text))

    def mainloop(self):
        self.window.mainloop()

    def refresh_board(self):
        for item in self.lines:
            self.canvas.delete(item)
        for item in self.game_end_text:
            self.canvas.delete(item)
        for item in self.items_dot:
            self.canvas.delete(item)

        for i in range(self.number_of_dots):
            x = i * self.distance_between_dots + self.distance_between_dots / 2
            self.canvas.create_line(x, self.distance_between_dots / 2, x,
                                    self.size_of_board - self.distance_between_dots / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(self.distance_between_dots / 2, x,
                                    self.size_of_board - self.distance_between_dots / 2, x,
                                    fill='gray', dash=(2, 2))

        self.dots = []
        for j in range(self.number_of_dots):
            temp = []
            for i in range(self.number_of_dots):
                start_x = i * self.distance_between_dots + self.distance_between_dots / 2
                end_x = j * self.distance_between_dots + self.distance_between_dots / 2

                color = self.dot_color
                outline_color = self.dot_color
                outline_width = 3
                if i == self.p1_starting_pos[1] and j == self.p1_starting_pos[0]:
                    color = self.dot_color_p1
                    outline_color = self.player1_color_light
                    outline_width = 5
                elif i == self.p2_starting_pos[1] and j == self.p2_starting_pos[0]:
                    color = self.dot_color_p2
                    outline_color = self.player2_color_light
                    outline_width = 1
                oval = self.canvas.create_oval(start_x - self.dot_width / 2, end_x - self.dot_width / 2, start_x + self.dot_width / 2,
                                               end_x + self.dot_width / 2, fill=color, outline=outline_color,
                                               width=outline_width)
                temp.append(oval)
            self.dots.append(temp)

    def check_position(self, player_current_position):
        player_current_position_x = player_current_position[0]
        player_current_position_y = player_current_position[1]

        possible_positions = []

        if player_current_position_x - 1 >= 0 and self.board_status[player_current_position_x - 1][player_current_position_y] == 0:
            possible_positions.append((player_current_position_x - 1, player_current_position_y))

        if player_current_position_x + 1 < self.number_of_dots and self.board_status[player_current_position_x + 1][player_current_position_y] == 0:
            possible_positions.append((player_current_position_x + 1, player_current_position_y))

        if player_current_position_y - 1 >= 0 and self.board_status[player_current_position_x][player_current_position_y - 1] == 0:
            possible_positions.append((player_current_position_x, player_current_position_y - 1))

        if player_current_position_y + 1 < self.number_of_dots and self.board_status[player_current_position_x][player_current_position_y + 1] == 0:
            possible_positions.append((player_current_position_x, player_current_position_y + 1))

        return possible_positions

    def is_over(self):
        # add if there are no way for two players
        p_1_possible_positions_len = len(self.check_position(self.player1_position))
        p_2_possible_positions_len = len(self.check_position(self.player2_position))

        # if p_1_possible_positions_len == 0:
        #     self.draw_board(self.player1_position, self.player1_position, self.dot_color_p1, self.player1_color_light,
        #                     self.player2_position, self.dot_color_p2, self.player2_color_light)
        #     self.player1_turn = False
        # elif p_2_possible_positions_len == 0:
        #     self.draw_board(self.player2_position, self.player2_position, self.dot_color_p2, self.player2_color_light,
        #                     self.player1_position, self.dot_color_p1, self.player1_color_light)
        #     self.player1_turn = True
        return np.count_nonzero(self.board_status == 0) == 0 or (p_1_possible_positions_len == 0 and p_2_possible_positions_len == 0)

    def callback(self):
        answer = mb.askyesno("Question", "Do you want to play again?")
        if answer:
            self.play_again()
        else:
            self.window.quit()

    def play(self):
        p1_positions = self.get_possible_positions(self.player1_position)
        p2_positions = self.get_possible_positions(self.player2_position)
        self.result = self.is_end(p1_positions + p2_positions)
        if self.result is not None:
            if self.result == player_2_indicator:
                print('The winner is Player 2!')
            elif self.result == player_1_indicator:
                print('The winner is Player 1!')
            elif self.result == 0:
                print("It's a tie!")
            return

        loading_text = self.canvas.create_text(400, 300, fill=self.dot_color_p2, font="Times 20 bold",
                                               text="Wait for AI to make it's move!")
        self.canvas.update_idletasks()

        while True:
            if self.player1_turn is False:
                (m, qx, qy) = self.min(self.player1_position, self.player2_position,
                                       -1 * (self.board_size * self.board_size), (self.board_size * self.board_size))
                self.board_status[qx][qy] = player_2_indicator
                self.draw_board(self.player2_position, (qx, qy), self.dot_color_p2, self.player2_color_light,
                                self.player1_position, self.dot_color_p1, self.player1_color_light)
                self.player2_position = (qx, qy)
                self.player1_turn = True

                self.player_2_score = self.square_count(self.player_2_value, self.board_status)
            p1_positions = self.get_possible_positions(self.player1_position)
            p2_positions = self.get_possible_positions(self.player2_position)
            if len(p1_positions) == 0 and len(p2_positions) > 0:
                self.player1_turn = False

            else:
                break

        self.canvas.delete(loading_text)

    def clicked(self, event):
        temp_user_name = self.entry1.get()
        if temp_user_name != "":
            self.user_name = temp_user_name
            self.canvas.delete("all")
            self.play_again()
            self.canvas.create_text(720, 490, fill="black", font="Times 15 bold", text="Instructions:")
            self.canvas.create_text(750, 530, fill="black", font="Times 12", text="=>  The red dot is you.")
            self.canvas.create_text(770, 570, fill="black", font="Times 12", text="=>  Move it with arrow keys.")
            self.canvas.create_text(780, 610, fill="black", font="Times 12", text="=>  Try to make as many squares")
            self.canvas.create_text(770, 640, fill="black", font="Times 12", text="as you can!")

        else:
            self.canvas.create_text(450, 350, text="Please enter a user name!", font="Times 20 bold",
                                    fill="red")

    def start_process(self):
        self.canvas.create_text(450, 200, fill="#00ff90", font="Times 50 bold", text="BOXES !!")

        self.canvas.create_text(350, 298, text="Enter a user name: ", font="Times 20 bold")

        buttonBG = self.canvas.create_rectangle(350, 400, 550, 460, fill="#57efff", outline="black")
        buttonTXT = self.canvas.create_text(450, 430, text="PLAY", font="Times 20 bold")

        self.entry1 = tk.Entry(self.canvas)
        self.canvas.create_window(550, 300, window=self.entry1)

        self.canvas.tag_bind(buttonBG, "<Button-1>", self.clicked)
        self.canvas.tag_bind(buttonTXT, "<Button-1>", self.clicked)

        minimax.mainloop()


minimax = Minimax(board_size)
minimax.start_process()
