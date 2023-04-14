from copy import deepcopy

class GoGame:
    def __init__(self, n):
        """
        Go game.
        :param n: size of the board n*n
        """
        self.size = n
        # self.X_move = True # X chess plays first
        self.died_pieces = []
        # self.n_move = 0
        self.max_move = n * n - 1
        self.komi = n/2 # Komi rule
        self.verbose = False # Verbose only when there is a manual player

    def init_board(self, n):
        board = [[0 for x in range(n)] for y in range(n)]  # Empty space marked as 0
        # 'X' pieces marked as 1
        # 'O' pieces marked as 2
        self.board = board
        self.previous_board = deepcopy(board)

    def set_board(self, piece_type, previous_board, board):
        """
        :param: 1(white piece - X) or 2(black piece - O).
        :return: None.
        """
        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == piece_type and board[i][j] != piece_type:
                    self.died_pieces.append((i, j))
        self.previous_board = previous_board
        self.board = board

    def copy_board(self):
        return deepcopy(self)

    def detect_neighbor(self, i, j):
        # board = self.board
        size = self.size
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return [point for point in neighbors if 0 < point[0] < size and 0 < point[1] < size]

    def detect_neighbor_group(self, i, j):
        """
        Find neighbors' with matched piece type
        :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
        """
        board = self.board
        all_neighbors = self.detect_neighbor(i, j)
        group_allies = []
        # Iterate through neighbors
        for stone in all_neighbors:
            # Add to allies list if having the same color
            if board[stone[0]][stone[1]] == board[i][j]:
                group_allies.append(stone)
        return group_allies

    def find_all_allies(self, i, j):
        q = []
        all_allies = []
        q.append((i, j))
        while q:
            piece = q.pop()
            all_allies.append(piece)
            neighbor_allies = self.detect_neighbor_group(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in q and ally not in all_allies:
                    q.append(ally)
        return all_allies

    def is_alive(self, i, j):
        """
        :return: boolean indicating whether the given stone still is dead.
        """
        board = self.board
        ally_members = self.find_all_allies(i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                if board[piece[0]][piece[1]] == 0:
                    return True
        return False

    def find_died_pieces(self, piece_type):
        """
        :return: a list containing the dead pieces row and column(row, column).
        """
        board = self.board
        dead_pieces = []
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == piece_type:
                    if not self.is_alive(i, j):
                        dead_pieces.append((i,j))
        return dead_pieces

    def remove_died_pieces(self, piece_type):
        """
        :return: locations of dead pieces.
        """
        dead_pieces = self.find_died_pieces(piece_type)
        if not dead_pieces:
            return []
        board = self.board
        for i in dead_pieces:
            board[i[0]][i[1]] = 0
        self.update_board(board)
        return dead_pieces

    def valid_place_check(self, i, j, piece_type, test_check=False):
        """
        :param test_check: boolean if it's a test check.
        :return: boolean indicating whether the placement is valid.
        """
        board = self.board
        verbose = self.verbose
        if test_check:
            verbose = False

        # Check if the place is in the board range
        if not (0 <= i < len(board)):
            if verbose:
                print(('Invalid placement. row should be range'))
            return False
        if not (0 <= j < len(board)):
            if verbose:
                print(('Invalid placement. column should range'))
            return False
        # Check if the place already has a piece
        if board[i][j] != 0:
            if verbose:
                print('Invalid placement. There is already a chess in this position.')
            return False

        # Copy the board for testing
        test_go = self.copy_board()
        test_board = test_go.board

        # Check if the place has liberty
        test_board[i][j] = piece_type
        test_go.update_board(test_board)
        if test_go.is_alive(i, j):
            return True

        # If no liberty found, remove the dead pieces of opponent and check again
        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.is_alive(i, j):
            if verbose:
                print('Invalid placement. No liberty found in this position.')
            return False

        # (KO rule)
        else:
            if self.died_pieces and self.compare_prev_cur_board(self.previous_board, test_go.board):
                if verbose:
                    print('Invalid placement. A repeat move not permitted by the KO rule.')
                return False
        return True

    def compare_prev_cur_board(self,board1, board2):
        for i in range(self.size):
            for j in range(self.size):
                if not board1[i][j] == board2[i][j]:
                    return False
        return True

    def place_chess(self, i, j, piece_type):
        '''
        :return: boolean indicating whether the placement is valid.
        '''
        board = self.board
        valid_place = self.valid_place_check(i, j, piece_type)
        if not valid_place:
            return False
        self.previous_board = deepcopy(board)
        board[i][j] = piece_type
        self.update_board(board)
        # Remove the following line for HW2 CS561 S2020
        # self.n_move += 1
        return True

    def update_board(self, new_board):
        """
        :param new_board: new board.
        :return: None.
        """
        self.board = new_board

    def game_end(self, piece_type, action="MOVE"):
        '''
        :param action: "MOVE" or "PASS".
        :return: boolean indicating whether the game should end.
        '''

        # Case 2: two players all pass the move.
        if self.compare_prev_cur_board(self.previous_board, self.board) and action == "PASS":
            return True
        return False

    def get_score(self, go, piece_type):
        count = 0
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == piece_type:
                    count += 1
        return count

    def judge_winner(self):
        player1 = self.score(1)
        player2 = self.score(2)
        if player1 > player2 + self.komi:
            return 1
        elif player1 < player2 + self.komi:
            return 2
        else:
            return 0
