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
            if event.keysym == "Up":
                new_player1_position_x = self.player1_position[0] - 1
                new_player1_position_y = self.player1_position[1]
                if self.player1_turn and new_player1_position_x >= 0 and self.board_status[new_player1_position_x][new_player1_position_y] != 2:
                    self.player1_position = (new_player1_position_x, new_player1_position_y)
                    self.board_status[new_player1_position_x][new_player1_position_y] = 1
            elif event.keysym == "Right":
                new_player1_position_x = self.player1_position[0]
                new_player1_position_y = self.player1_position[1] + 1
                if self.player1_turn and new_player1_position_y < number_of_dots and self.board_status[new_player1_position_x][new_player1_position_y] != 2:
                    self.player1_position = (new_player1_position_x, new_player1_position_y)
                    self.board_status[new_player1_position_x][new_player1_position_y] = 1
            elif event.keysym == "Down":
                new_player1_position_x = self.player1_position[0] + 1
                new_player1_position_y = self.player1_position[1]
                if self.player1_turn and new_player1_position_x < number_of_dots and self.board_status[new_player1_position_x][new_player1_position_y] != 2:
                    self.player1_position = (new_player1_position_x, new_player1_position_y)
                    self.board_status[new_player1_position_x][new_player1_position_y] = 1
            elif event.keysym == "Left":
                new_player1_position_x = self.player1_position[0]
                new_player1_position_y = self.player1_position[1] - 1
                if self.player1_turn and new_player1_position_y >= 0 and self.board_status[new_player1_position_x][new_player1_position_y] != 2:
                    self.player1_position = (new_player1_position_x, new_player1_position_y)
                    self.board_status[new_player1_position_x][new_player1_position_y] = 1
        print(self.board_status)

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

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - distance_between_dots / 4) // (distance_between_dots / 2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            logical_position = [r, c]
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------
    #
    # def make_edge(self, type, logical_position):
    #     if type == 'row':
    #         start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
    #         end_x = start_x + distance_between_dots
    #         start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
    #         end_y = start_y
    #     elif type == 'col':
    #         start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
    #         end_y = start_y + distance_between_dots
    #         start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
    #         end_x = start_x
    #
    #     if self.player1_turn:
    #         color = player1_color
    #     else:
    #         color = player2_color
    #     self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)

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

    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width / 2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width / 2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')


game_instance = BoxesGame()
game_instance.mainloop()
