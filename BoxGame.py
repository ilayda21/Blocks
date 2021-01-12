from tkinter import *
from tkinter import messagebox as mb

import numpy as np
import numpy.linalg as deter

class BoxesGame:
    def __init__(self, board_size):
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
        self.player2_position = (self.number_of_dots - 1, self.number_of_dots - 1)
        self.player1_position = (0, 0)
        self.window = Tk()
        self.window.title('Boxes')
        self.canvas = Canvas(self.window, width=self.size_of_board + 200, height=self.size_of_board)
        self.canvas.pack()
        self.player1_turn = True
        self.score_items = []
        self.lines = []
        self.items_dot = []
        self.game_end_text = []
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
                    self.draw_board(self.player1_position, new_position, self.dot_color_p1, self.player1_color_light,
                                    self.player2_position, self.dot_color_p2, self.player2_color_light)
                    self.player1_position = new_position
                    self.player1_turn = False

                self.player_1_score = self.square_count(self.player_1_value, self.board_status)

            else:
                result_position_info = self.update_position(event.keysym, self.player2_position, False)
                if result_position_info[0]:
                    new_position = (result_position_info[1], result_position_info[2])
                    self.draw_board(self.player2_position, new_position, self.dot_color_p2, self.player2_color_light,
                                    self.player1_position, self.dot_color_p1, self.player1_color_light)
                    self.player2_position = new_position
                    self.player1_turn = True

                self.player_2_score = self.square_count(self.player_2_value, self.board_status)
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
                self.board_status[new_player_position_x][new_player_position_y] = current_player_indicator
                is_valid = True
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
        self.player2_position = (self.number_of_dots - 1, self.number_of_dots - 1)
        self.player1_position = (0, 0)
        self.board_status[0][0] = self.player_1_value
        self.board_status[self.number_of_dots - 1][self.number_of_dots - 1] = self.player_2_value
        self.create_score_board(str(0), str(0))

        self.refresh_board()

    def create_score_board(self, player_1_score, player_2_score):
        for item in self.score_items:
            self.canvas.delete(item)
        self.score_items.append(self.canvas.create_text(750, 60, fill=self.dot_color_p1, font="Times 20 bold",
                                                        text="Player 1:"))
        self.score_items.append(self.canvas.create_text(820, 60, fill="black", font="Times 20 bold",
                                                        text=player_1_score))
        self.score_items.append(self.canvas.create_text(750, 100, fill=self.dot_color_p2, font="Times 20 bold",
                                                        text="Player 2:"))
        self.score_items.append(self.canvas.create_text(820, 100, fill="black", font="Times 20 bold",
                                                        text=player_2_score))

    def create_game_end_panel(self, player_1_score, player_2_score):
        text = ""
        if player_2_score < player_1_score:
            text = "Player 1 \n Wins ! "
        elif player_1_score < player_2_score:
            text = "Player 2 \n  Wins !"
        elif player_1_score == player_2_score:
            text = "  It is \na TIE !"

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
                if i == 0 and j == 0:
                    color = self.dot_color_p1
                    outline_color = self.player1_color_light
                    outline_width = 5
                elif i == self.number_of_dots - 1 and j == self.number_of_dots - 1:
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

        if p_1_possible_positions_len == 0:
            self.player1_turn = False
            self.draw_board(self.player1_position, self.player1_position, self.dot_color_p1, self.player1_color_light,
                            self.player2_position, self.dot_color_p2, self.player2_color_light)
        elif p_2_possible_positions_len == 0:
            self.player1_turn = True
            self.draw_board(self.player2_position, self.player2_position, self.dot_color_p2, self.player2_color_light,
                            self.player1_position, self.dot_color_p1, self.player1_color_light)
        return np.count_nonzero(self.board_status == 0) == 0 or (p_1_possible_positions_len == 0 and p_2_possible_positions_len == 0)

    def square_count(self, val, board_status):
        turn = val
        p1_count = 0
        p2_count = 0
        bigger_matrix = self.number_of_dots
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

    def callback(self):
        answer = mb.askyesno("Question", "Do you want to play again?")
        if answer:
            self.play_again()
        else:
            self.window.quit()

