def _min(self, go, piece_type, depth):
    state = self.encode_board(go)
    if state in self.transition:
        return self.transition[state]
    if go.game_end(piece_type):
        if go.judge_winner() == 0:
            return (DRAW_REWARD, None)
        if go.judge_winner() == piece_type:
            return (float('inf'), None)
        else:
            return float('-inf'), None
    else:
        min_value, action = float('inf'), None
        # candidates = [(i, j) for i in range(go.size) if go.board[i][j] == 0 for j in range(go.size)]
        candidates = []
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == 0:
                    candidates.append((i, j))
        for i, j in candidates:
            copyBoard = go.board
            if piece_type == 1:
                opponent = 2
            else:
                opponent = 1
            if go.place_chess(i, j, opponent):
                go.remove_died_pieces(opponent)
                go.remove_died_pieces(piece_type)
                score, a = self._max(go, piece_type, depth)
                if score < min_value or action == None:
                    min_value, action = go.score(piece_type) + self.liberty_degree(go, piece_type)*30\
                                        + self.neighbor_degree(i, j) - self.liberty_degree(go, 3-piece_type)*15\
                                        +self.freedom_degree(go, piece_type, i, j), (i, j)
                    self.transition[state] = (min_value, action)
                self.transition[state] = (min_value, action)
        # print("min: ", end='')
        # print(min_value, action)
        return (min_value, action)

def _max(self, go, piece_type, depth):
    # FIXME: fix here
    # test_go = go.copy_board()
    # print(test_go.board)
    state = self.encode_board(go)
    if state in self.transition:
        return self.transition[state]
    # end of FIXME
    if go.game_end(piece_type):
        if go.judge_winner() == 0:
            return (DRAW_REWARD, None)
        if go.judge_winner() == piece_type:
            return (float('inf'), None)
        else:
            return float('-inf'), None
    # game NOT end yet
    else:
        '''
        if depth == LEVEL:
            max_value, action = DRAW_REWARD, None
            # candidates = [(i, j) for i in range(go.size) if go.board[i][j] == 0 for j in range(go.size)]
            candidates = []
            for i in range(go.size):
                for j in range(go.size):
                    if go.board[i][j] == 0:
                        candidates.append((i, j))
            for i, j in candidates:
                if go.place_chess(i, j, piece_type):
                    go.remove_died_pieces(piece_type)
                    go.remove_died_pieces(3 - piece_type)
                    score = go.score(piece_type)
                    a = (i, j)
                    # score, a = self._min(go, piece_type, depth)
                    if score > max_value or action == None:
                        # TODO: add liberty for max_value
                        # max_value, action = score, (i, j)
                        max_value, action = go.score(piece_type) + self.liberty_degree(go, piece_type), (i, j)
                        # if max_value > DRAW_REWARD:
                        self.transition[state] = (max_value, action)
                    self.transition[state] = (max_value, action)

            return max_value, action
            # print(self.transition)
            # return max(self.transition.values())[0], max(self.transition.values())[1]
        else:
        '''
        max_value, action = float('-inf'), None
        # candidates = [(i, j) for i in range(go.size) if go.board[i][j] == 0 for j in range(go.size)]
        candidates = []
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == 0:
                    candidates.append((i, j))
        for i, j in candidates:
            # print("1: ")
            # print(go.board)
            # print("score: ", end='')
            # print(go.score(piece_type))
            # print("liberty: ", end='')
            # print(self.liberty_degree(go, piece_type))
            if go.place_chess(i, j, piece_type):
                go.remove_died_pieces(piece_type)
                go.remove_died_pieces(3 - piece_type)
                # print("2: ")
                # print(go.board)
                # print("score: ", end='')
                # print(go.score(piece_type))
                # print("liberty: ", end='')
                # print(self.liberty_degree(go, piece_type))
                if not depth == LEVEL:
                    score, a = self._min(go, piece_type, depth+1)
                else:
                    score = go.score(piece_type)
                    a = (i, j)
                if score > max_value or action == None:
                    max_value, action = go.score(piece_type) + self.liberty_degree(go, piece_type)*30\
                                        + self.neighbor_degree(i, j) - self.liberty_degree(go, 3-piece_type)*15\
                                        +self.freedom_degree(go, piece_type, i, j), (i, j)
                    # if max_value > DRAW_REWARD:
                    self.transition[state] = (max_value, action)
                self.transition[state] = (max_value, action)
        # test = max(self.transition.values())
        # print(list(self.transition.values())[list(self.transition.values()).index(test[0])])
        # print(test)
        # print("max: ", end='')
        # print(max_value, action)
        return max_value, action

'''

=====================================================================

'''
    def _minimax(self, go, piece_type, is_max_turn, current_depth, row=None, col=None):
        if current_depth == MAX_DEPTH or go.game_end(piece_type):
            if go.game_end(piece_type):
                if go.judge_winner() == 0:
                    return (DRAW_REWARD, None)
                if go.judge_winner() == piece_type:
                    return WIN_REWARD, None
                else:
                    return LOSS_REWARD, None

            # return go.score(piece_type) + self.liberty_degree(go, piece_type) * 30\
            #     + self.neighbor_degree(row, col) \
            #     - self.liberty_degree(go, 3-piece_type) * 15\
            #     + self.freedom_degree(go, piece_type, row, col), (row, col)
            return go.score(piece_type), (row, col)

            # TODO: write a fuction for evaluation function
            # return evaluation_function(go, piece_type), None

        copy_go = go.copy_board()
        best_value = float('-inf') if is_max_turn else float('inf')
        action = None
        if
        # candidates = [(i, j) for i in range(go.size) if go.board[i][j] == 0 for j in range(go.size)]
        candidates = []
        for i in range(copy_go.size):
            for j in range(copy_go.size):
                if copy_go.valid_place_check(i, j, piece_type, test_check = True):
                    candidates.append((i, j))
        random.shuffle(candidates)  # randomness
        # print(bool(candidates), candidates)
        # if not candidates:
        #     return 0, "PASS"
        # else:
        for i, j in candidates:
            # print("previous state: ")
            # print(go.board)
            # print("score: ", end='')
            # print(go.score(piece_type))
            # print("liberty: ", end='')
            # print(self.liberty_degree(go, piece_type))
            # print(i,j)
            print(copy_go.board)

            if copy_go.place_chess(i, j, piece_type):
                # go.remove_died_pieces(piece_type)
                copy_go.remove_died_pieces(3 - piece_type)
                copy_go.board
                # print("current state: ")
                # print(go.board)
                # print("score: ", end='')
                # print(go.score(piece_type))
                # print("liberty: ", end='')
                # print(self.liberty_degree(go, piece_type))

                eval_child, action_child = self._minimax(copy_go, piece_type, not is_max_turn, current_depth+1, i, j)

                if is_max_turn and best_value < eval_child:
                    best_value = eval_child
                    action = action_child
                elif (not is_max_turn) and best_value > eval_child:
                    best_value = eval_child
                    action = action_child
        # print("max: " if is_max_turn else "min: ", end='')
        # print(best_value, action)
        return best_value, action

    '''
    
    =====================================================================
    
    '''
    def _min(self, go, piece_type, depth, alpha, beta):
        # state = self.encode_board(go)
        # if state in self.transition:
        #     return self.transition[state]
        if go.game_end(piece_type):
            if go.judge_winner() == 0:
                return (DRAW_REWARD, None)
            if go.judge_winner() == piece_type:
                return (float('inf'), None)
            else:
                return float('-inf'), None
        if depth == MAX_DEPTH:
            return go.score(piece_type) + self.liberty_degree(go, piece_type)*30\
                                        - self.liberty_degree(go, 3-piece_type)*15\
                                        , None
        min_value, action = float('inf'), None
        candidates = []
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == 0:
                    candidates.append((i, j))
        for i, j in candidates:
            copyBoard = go.board
            if piece_type == 1:
                opponent = 2
            else:
                opponent = 1
            if go.place_chess(i, j, opponent):
                go.remove_died_pieces(opponent)
                go.remove_died_pieces(piece_type)
                score, a = self._max(go, piece_type, depth+1, alpha, beta)
                if score < min_value or action == None:
                    min_value = score
                    action = (i, j)
                    # self.transition[state] = (min_value, action)
                if min_value < alpha:
                    return min_value, action

                if min_value < beta:
                    beta = min_value
                # self.transition[state] = (min_value, action)
        # print("min: ", end='')
        # print(min_value, action)
        return min_value, action

    def _max(self, go, piece_type, depth, alpha, beta):
        '''state = self.encode_board(go)
        if state in self.transition:
            return self.transition[state]'''
        if go.game_end(piece_type):
            if go.judge_winner() == 0:
                return (DRAW_REWARD, None)
            if go.judge_winner() == piece_type:
                return (float('inf'), None)
            else:
                return float('-inf'), None
        if depth == MAX_DEPTH:
            return go.score(piece_type) + self.liberty_degree(go, piece_type)*30\
                                        - self.liberty_degree(go, 3-piece_type)*15, None

        max_value, action = float('-inf'), None
        candidates = []
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == 0:
                    candidates.append((i, j))
        for i, j in candidates:
            # print("1: ")
            # print(go.board)
            # print("score: ", end='')
            # print(go.score(piece_type))
            # print("liberty: ", end='')
            # print(self.liberty_degree(go, piece_type))
            if go.place_chess(i, j, piece_type):
                go.remove_died_pieces(3 - piece_type)
                # print("2: ")
                # print(go.board)
                # print("score: ", end='')
                # print(go.score(piece_type))
                # print("liberty: ", end='')
                # print(self.liberty_degree(go, piece_type))
                score, action = self._min(go, piece_type, depth, alpha, beta)
                if score > max_value or action == None:
                    max_value = score
                    action = (i, j)
                    # if max_value > DRAW_REWARD:
                    # self.transition[state] = (max_value, action)
                if max_value > beta:
                    return max_value, action

                if max_value > alpha:
                    alpha = max_value
                # self.transition[state] = (max_value, action)
        # test = max(self.transition.values())
        # print(list(self.transition.values())[list(self.transition.values()).index(test[0])])
        # print(test)
        # print("max: ", end='')
        # print(max_value, action)
        return max_value, action

'''
    
=====================================================================================================================

'''
import random
import sys
from read import readInput
from write import writeOutput

from host import GO
import random

WIN_REWARD = 10000
DRAW_REWARD = 0.0
LOSS_REWARD = -10000
MAX_DEPTH = 5

class MyPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, go, piece_type):
        '''
        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))

        if not possible_placements:
            return "PASS"
        elif len(possible_placements) == go.size * go.size:
            return (int(go.size/2), int(go.size/2))
        else:
            score, action = self._max(go, piece_type, 0, float("-inf"), float("inf"))
            print("score: ", score)
            print("action: ", action)
            return action
    '''
    
    Strarting here:
    
    '''
    def encode_board(self, go):
        """ Encode the current state of the board as a string
        """
        return ''.join([str(go.board[i][j]) for i in range(go.size) for j in range(go.size)])

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

    def freedom_degree(self, go, piece_type, i, j):
        neighbors = go.detect_neighbor(i, j)
        for n in neighbors:
            if go.board[n[0]][n[1]] == piece_type:
                p = n[0] - 1
                q = n[1] - j
                if (p, q) == (-1, -1) or (p, q) == (-1, 1) or (p, q) == (1, -1) or (p, q) == (1, 1):
                    return 25
        return 0

    def neighbor_degree(self, i, j):
        count = len(go.detect_neighbor(i, j)) * 3
        return count

    def evaluation(self, go, piece_type, dead_pieces_num):
        # if len(possible_position) >= 21:
        return go.score(piece_type) + \
               3*(self.liberty_degree(go, piece_type) - self.liberty_degree(go, 3-piece_type)) + \
               10*dead_pieces_num

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
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == 0:
                    candidates.append((i, j))
        for i, j in candidates:
            copyBoard = go.board
            if piece_type == 1:
                opponent = 2
            else:
                opponent = 1
            if go.place_chess(i, j, opponent):
                dead_pieces = go.find_died_pieces(piece_type)
                # go.remove_died_pieces(opponent)
                go.remove_died_pieces(piece_type)
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
                if go.board[i][j] == 0:
                    candidates.append((i, j))
        for i, j in candidates:
            # print("1: ")
            # print(go.board)
            # print("score: ", end='')
            # print(go.score(piece_type))
            # print("liberty: ", end='')
            # print(self.liberty_degree(go, piece_type))
            if go.place_chess(i, j, piece_type):
                dead_pieces = go.find_died_pieces(3 - piece_type)
                go.remove_died_pieces(3 - piece_type)
                # print("2: ")
                # print(go.board)
                # print("score: ", end='')
                # print(go.score(piece_type))
                # print("liberty: ", end='')
                # print(self.liberty_degree(go, piece_type))
                score, action = self._min(go, piece_type, depth, alpha, beta, len(dead_pieces))
                if score > max_value:
                    max_value = score
                    action = (i, j)
                    # if max_value > DRAW_REWARD:
                    # self.transition[state] = (max_value, action)
                if max_value > beta:
                    return max_value, action

                if max_value > alpha:
                    alpha = max_value
        return max_value, action

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = MyPlayer()
    action = player.get_input(go, piece_type)
    writeOutput(action)
