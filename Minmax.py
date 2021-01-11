import numpy as np
import numpy.linalg as deter

board_size = 6
player_1_indicator = 1
player_2_indicator = 5


class Game:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.current_state = np.zeros(shape=(board_size, board_size))

        self.player_1_position = (0, 0)
        self.player_2_position = (board_size - 1, board_size - 1)

        self.current_state[0][0] = player_1_indicator
        self.current_state[board_size - 1][board_size - 1] = player_2_indicator

        # Player X always plays first
        self.player_turn = player_1_indicator

    def draw_board(self):
        for i in range(0, board_size):
            for j in range(0, board_size):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    def square_count(self, val, board_status):
        turn = val
        p1_count = 0
        p2_count = 0
        bigger_matrix = board_size
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
        if np.count_nonzero(self.current_state == 0) == 0 or len(possible_positions) == 0:
            p_1_count = self.square_count(player_1_indicator, self.current_state)
            p_2_count = self.square_count(player_2_indicator, self.current_state)

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
        if current_player_position_x - 1 >= 0 and self.current_state[current_player_position_x - 1][current_player_position_y] == 0:
            possible_positions.append((current_player_position_x - 1, current_player_position_y))

        if current_player_position_x + 1 < board_size and self.current_state[current_player_position_x + 1][current_player_position_y] == 0:
            possible_positions.append((current_player_position_x + 1, current_player_position_y))

        if current_player_position_y - 1 >= 0 and self.current_state[current_player_position_x][current_player_position_y - 1] == 0:
            possible_positions.append((current_player_position_x, current_player_position_y - 1))

        if current_player_position_y + 1 < board_size and self.current_state[current_player_position_x][current_player_position_y + 1] == 0:
            possible_positions.append((current_player_position_x, current_player_position_y + 1))

        filtered_possible_position = []
        for possible_position in possible_positions:
            pos_x = possible_position[0]
            pos_y = possible_position[1]
            #   +
            # + + +
            #   +
            if pos_x - 1 >= 0 and pos_x + 1 < board_size and pos_y + 1 < board_size and pos_y - 1 >= 0:
                if self.current_state[pos_x - 1][pos_y] != 0 and self.current_state[pos_x + 1][pos_y] != 0 and self.current_state[pos_x][pos_y + 1] != 0 and \
                        self.current_state[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            # + +
            # +
            #
            elif pos_x + 1 < board_size and pos_y + 1 < board_size:
                if self.current_state[pos_x + 1][pos_y] != 0 and self.current_state[pos_x][pos_y + 1] != 0:
                    filtered_possible_position.append(possible_position)
            #   + +
            #     +
            #
            elif pos_x - 1 >= 0 and pos_y + 1 < board_size:
                if self.current_state[pos_x - 1][pos_y] != 0 and self.current_state[pos_x][pos_y + 1] != 0:
                    filtered_possible_position.append(possible_position)
            #
            # +
            # + +
            elif pos_x + 1 < board_size and pos_y - 1 >= 0:
                if self.current_state[pos_x + 1][pos_y] != 0 and self.current_state[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            #
            #     +
            #   + +
            elif pos_x - 1 >= 0 and pos_y - 1 >= 0:
                if self.current_state[pos_x - 1][pos_y] != 0 and self.current_state[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            #  +
            #  + +
            #  +
            elif pos_x + 1 < board_size and pos_y + 1 < board_size and pos_y - 1 >= 0:
                if self.current_state[pos_x + 1][pos_y] != 0 and self.current_state[pos_x][pos_y + 1] != 0 and self.current_state[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            #  + + +
            #    +
            #
            elif pos_x - 1 >= 0 and pos_x + 1 < board_size and pos_y + 1 < board_size:
                if self.current_state[pos_x - 1][pos_y] != 0 and self.current_state[pos_x + 1][pos_y] != 0 and self.current_state[pos_x][pos_y + 1] != 0:
                    filtered_possible_position.append(possible_position)
            #     +
            #   + +
            #     +
            elif pos_x - 1 >= 0 and pos_y + 1 < board_size and pos_y - 1 >= 0:
                if self.current_state[pos_x - 1][pos_y] != 0 and self.current_state[pos_x][pos_y + 1] != 0 and self.current_state[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)
            #
            #    +
            #  + + +
            elif pos_x - 1 >= 0 and pos_x + 1 < board_size and pos_y - 1 >= 0:
                if self.current_state[pos_x - 1][pos_y] != 0and self.current_state[pos_x][pos_y + 1] != 0 and self.current_state[pos_x][pos_y - 1] != 0:
                    filtered_possible_position.append(possible_position)

        f_result = set(possible_positions) - set(filtered_possible_position)
        if len(f_result) > 0:
            possible_positions = list(f_result)
        return possible_positions

    # Player player_1 is max
    def max(self, current_p1_position, current_p2_position, alpha, beta):
        # print("++++++++++++++++++++++++++++++++++++++++++++")
        # print("+MAX : Player 1")
        # Possible values for maxv are:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        # We're initially setting it to -2 as worse than the worst case:
        maxv = -2

        px = None
        py = None

        possible_positions = self.get_possible_positions(current_p1_position)
        # print("+ POSSIBLE POSITIONS:")
        # print(possible_positions)
        result = self.is_end(possible_positions)
        # print("+ RESULT: ")
        # print(result)
        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win
        if result == player_2_indicator:
            return (-1, 0, 0)
        elif result == player_1_indicator:
            return (1, 0, 0)
        elif result == 0:
            return (0, 0, 0)

        for position in possible_positions:
            # print("++ position: ")
            # print(position)
            i = position[0]
            j = position[1]
            self.current_state[i][j] = player_1_indicator

            # print("++ Current State:")
            # self.draw_board()
            (m, min_i, min_j) = self.min((i, j), current_p2_position, alpha, beta)
            # Fixing the maxv value if needed
            # print("++ m: " + str(m) + " - maxv" + str(maxv))
            if m > maxv:
                maxv = m
                px = i
                py = j
            # Setting back the field to empty
            self.current_state[i][j] = 0

            if maxv >= beta:
                return maxv, px, py

            if maxv > alpha:
                alpha = maxv
            # print("++ returned current state")
            # self.draw_board()
        # print("++++++++++++++++++++++++++++++++++++++++++++")
        return maxv, px, py

    # Player 'player 2' is min
    def min(self, current_p1_position, current_p2_position, alpha, beta):
        # print("--------------------------------------------")
        # print("- MIN : Player 2")
        # Possible values for minv are:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # We're initially setting it to 2 as worse than the worst case:
        minv = 2

        qx = None
        qy = None
        possible_positions = self.get_possible_positions(current_p2_position)
        # print("- POSSIBLE POSITIONS:")
        # print(possible_positions)
        result = self.is_end(possible_positions)
        # print("- RESULT: ")
        # print(result)

        if result == player_2_indicator:
            return (-1, current_p2_position[0], current_p2_position[1])
        elif result == player_1_indicator:
            return (1, current_p2_position[0], current_p2_position[1])
        elif result == 0:
            return (0, current_p2_position[0], current_p2_position[1])

        for position in possible_positions:
            # print("-- position: ")
            # print(position)
            i = position[0]
            j = position[1]
            self.current_state[i][j] = player_2_indicator

            # print("-- Current State:")
            # self.draw_board()

            (m, max_i, max_j) = self.max(current_p1_position, (i, j), alpha, beta)
            # print("-- m: " + str(m) + " - minv" + str(minv))
            if m < minv:
                minv = m
                qx = i
                qy = j
            self.current_state[i][j] = 0

            if minv <= alpha:
                return minv, qx, qy

            if minv < beta:
                beta = minv
            # print("-- returned current state")
            # self.draw_board()
        # print("--------------------------------------------")
        return minv, qx, qy

    def play(self):
        while True:
            self.draw_board()

            p1_positions = self.get_possible_positions(self.player_1_position)
            p2_positions = self.get_possible_positions(self.player_2_position)
            self.result = self.is_end(p1_positions + p2_positions)

            # Printing the appropriate message if the game has ended
            if self.result != None:
                if self.result == player_2_indicator:
                    print('The winner is Player 2!')
                elif self.result == player_1_indicator:
                    print('The winner is Player 1!')
                elif self.result == 0:
                    print("It's a tie!")

                self.initialize_game()
                return

            # If it's player's turn
            if self.player_turn == player_2_indicator:
                (m, qx, qy) = self.min(self.player_1_position, self.player_2_position, -2, 2)
                self.current_state[qx][qy] = player_2_indicator
                self.player_turn = player_1_indicator
                self.player_2_position = (qx, qy)

            # If it's AI's turn
            else:
                (m, px, py) = self.max(self.player_1_position, self.player_2_position,-2, 2)
                self.current_state[px][py] = player_1_indicator
                self.player_turn = player_2_indicator
                self.player_1_position = (px, py)


g = Game()
g.play()
