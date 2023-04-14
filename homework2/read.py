
def readInput(n, path="input.txt"):
    with open(path, 'r') as file:
        lines = file.readlines()
        piece_type = int(lines[0])
        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        current_board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, current_board

def readOutput(path="output.txt"):
    with open(path, 'r') as file:
        position = file.readline().strip().split(',')

        if position[0] == "PASS":
            return "PASS", -1, -1
        x = int(position[0])
        y = int(position[1])

    return "MOVE", x, y
