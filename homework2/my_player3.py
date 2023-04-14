import random
import sys
from copy import deepcopy
from read import readInput
from write import writeOutput
from host import GO
from go_game import GoGame

WIN_REWARD = 1000
DRAW_REWARD = 0.0
LOSS_REWARD = -1000
MAX_DEPTH = 3

class MyPlayer():
    def __init__(self):
        self.type = 'myplayer'

    def get_input(self, go, piece_type):
        # :param piece_type: 1('X') or 2('O').
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))
        possile_size = len(possible_placements)
        total_positions = go.size * go.size

        if not possible_placements:
            return "PASS"
        elif possile_size == total_positions:
            return int(go.size/2), int(go.size/2)
        elif possile_size == total_positions-1 and go.valid_place_check(int(go.size/2), int(go.size/2), piece_type, test_check = True):
            return int(go.size/2), int(go.size/2)
        else:
            score, action = self._max(go, piece_type, 0, float("-inf"), float("inf"))
            # action = self.greedy(go, piece_type)
            # print("score: ", score)
            # print("action: ", action)
            return action

    def find_neighbors(self, go, i, j):
        """ :return number of neighbors at given location """
        size = go.size
        count_neighbors = 0
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        neighbors = [point for point in neighbors if 0 < point[0] < size and 0 < point[1] < size]
        for p, q in neighbors:
            if go.board[p][j] == 0:
                count_neighbors += 1
        return count_neighbors

    def liberty_degree(self, go, piece_type):
        count_liberty = 0
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == piece_type:
                    # if (i, j) in visited:
                    #     continue
                    # else:
                    count_liberty += self.find_neighbors(go, i, j)
        return count_liberty

    # def freedom_degree(self, go, piece_type, i, j):
    #     neighbors = go.detect_neighbor(i, j)
    #     for n in neighbors:
    #         if go.board[n[0]][n[1]] == piece_type:
    #             p = n[0] - 1
    #             q = n[1] - j
    #             if (p, q) == (-1, -1) or (p, q) == (-1, 1) or (p, q) == (1, -1) or (p, q) == (1, 1):
    #                 return 25
    #     return 0

    def neighbor_degree(self, i, j):
        count = len(go.detect_neighbor(i, j)) * 3
        return count

    def get_score(self, go, piece_type):
        count = 0
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == piece_type:
                    count += 1
        return count

    def evaluation(self, go, piece_type, dead_pieces_num):
        # if len(possible_position) >= 21:
        return self.get_score(go, piece_type)+ \
               3*(self.liberty_degree(go, piece_type) - self.liberty_degree(go, 3-piece_type)) + \
               4*dead_pieces_num

    def _min(self, go, piece_type, depth, alpha, beta, dead_pieces_num=0):
        if go.game_end(piece_type):
            if go.judge_winner() == 0:
                return (DRAW_REWARD, None)
            if go.judge_winner() == piece_type:
                return (float('inf'), None)
            else:
                return float('-inf'), None
        if depth == MAX_DEPTH:
            return self.evaluation(go, piece_type, dead_pieces_num), None

        min_value, action = float('inf'), None
        candidates = []
        if piece_type == 1:
            opponent = 2
        else:
            opponent = 1
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, opponent, test_check=True):
                    candidates.append((i, j))

        for i, j in candidates:
            # copy_go = deepcopy(go)
            if go.valid_place_check(i, j, opponent, test_check=True):
                if go.place_chess(i, j, opponent):
                    go.update_board(go.board)
                    # dead_pieces = []
                    dead_pieces = go.find_died_pieces(piece_type)
                    # go.remove_died_pieces(opponent)
                    # go.remove_died_pieces(piece_type)
                    # go.update_board(go.board)
                    score, a = self._max(go, piece_type, depth+1, alpha, beta, len(dead_pieces))
                    if score < min_value:
                        min_value = score
                        action = (i, j)
                    if min_value < alpha:
                        return min_value, action
                    if min_value < beta:
                        beta = min_value

        return min_value, action

    def _max(self, go, piece_type, depth, alpha, beta, dead_pieces_num=0):
        if go.game_end(piece_type):
            if go.judge_winner() == 0:
                return (DRAW_REWARD, None)
            if go.judge_winner() == piece_type:
                return (float('inf'), None)
            else:
                return float('-inf'), None
        if depth == MAX_DEPTH:
            return self.evaluation(go, piece_type, dead_pieces_num), None

        max_value, action = float('-inf'), None
        candidates = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check=True):
                    candidates.append((i, j))
        for i, j in candidates:
            # copy_go = deepcopy(go)
            if go.valid_place_check(i, j, piece_type, test_check=True):
                if go.place_chess(i, j, piece_type):
                    go.update_board(go.board)
                    # dead_pieces = []
                    dead_pieces = go.find_died_pieces(3 - piece_type)
                    # go.remove_died_pieces(3 - piece_type)
                    # go.update_board(go.board)

                    score, action = self._min(go, piece_type, depth, alpha, beta, len(dead_pieces))
                    if score > max_value:
                        max_value = score
                        action = (i, j)

                    if max_value > beta:
                        return max_value, action

                    if max_value > alpha:
                        alpha = max_value
        return max_value, action

    def greedy(self, go, piece_type):
        max_value = 0
        position = None
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))
        for stone in possible_placements:
            copy_go = go.copy_board()
            copy_go.place_chess(stone[0], stone[1], piece_type)
            dead_stone = copy_go.remove_died_pieces(3 - piece_type)

            score = self.cal_score(copy_go, piece_type, len(dead_stone))
            if score > max_value:
                max_value = score;
                position = stone
        return position

    def cal_score(self, go, piece_type, dead_stone_num):
        count = 0
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == piece_type:
                    count += 1
        count += dead_stone_num
        return count

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GoGame(N)
    go.set_board(piece_type, previous_board, board)
    player = MyPlayer()
    action = player.get_input(go, piece_type)
    writeOutput(action)
