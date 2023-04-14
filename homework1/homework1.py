from collections import deque
from operator import add
import heapq
import math


class Homework1:
    NATURAL_NUMBER_TO_INDEX = -1
    _actions = (
        (1, 0, 0),      # 1: X+
        (-1, 0, 0),     # 2: X-
        (0, 1, 0),      # 3: Y+
        (0, -1, 0),     # 4: Y-
        (0, 0, 1),      # 5: Z+
        (0, 0, -1),     # 6: Z-
        (1, 1, 0),      # 7: X+ Y+
        (1, -1, 0),     # 8: X+ Y-
        (-1, 1, 0),     # 9: X- Y+
        (-1, -1, 0),    # 10: X- Y-
        (1, 0, 1),      # 11: X+ Z+
        (1, 0, -1),     # 12: X+ Z-
        (-1, 0, 1),     # 13: X- Z+
        (-1, 0, -1),    # 14: X- Z-
        (0, 1, 1),      # 15: Y+ Z+
        (0, 1, -1),     # 16: Y+ Z-
        (0, -1, 1),     # 17: Y- Z+
        (0, -1, -1)     # 18: Y- Z-
    )

    class Grid:
        def __init__(self, loc, cost, heuristic=None, past_cost=None):
            self.location = loc
            self.cost = cost
            self.heuristic = heuristic
            self.past_cost = past_cost

        def __eq__(self, other):
            if self.heuristic is None:
                return self.cost == other.cost
            else:
                return (self.past_cost + self.heuristic) == (other.past_cost + other.heuristic)

        def __hash__(self):
            return hash(self.location)

        def __ne__(self, other):
            if self.heuristic is None:
                return self.cost != other.cost
            else:
                return (self.past_cost + self.heuristic) != (other.past_cost + other.heuristic)

        def __lt__(self, other):
            if self.heuristic is None:
                return self.cost < other.cost
            else:
                return (self.past_cost + self.heuristic) < (other.past_cost + other.heuristic)

        def __le__(self, other):
            if self.heuristic is None:
                return self.cost <= other.cost
            else:
                return (self.past_cost + self.heuristic) <= (other.past_cost + other.heuristic)

        def __gt__(self, other):
            if self.heuristic is None:
                return self.cost > other.cost
            else:
                return (self.past_cost + self.heuristic) > (other.past_cost + other.heuristic)

        def __ge__(self, other):
            if self.heuristic is None:
                return self.cost >= other.cost
            else:
                return (self.past_cost + self.heuristic) >= (other.past_cost + other.heuristic)

    @staticmethod
    def write_result(file_stream, exit_grid_with_cost, child_parent, fail=False):
        if fail:
            print("FAIL", file=file_stream, end='')
            return
        result = deque()
        result.append(exit_grid_with_cost)
        parent = child_parent[exit_grid_with_cost[:-1]]
        cost = exit_grid_with_cost[len(exit_grid_with_cost) - 1]    # last index is "cost"
        while parent is not None:
            result.append(parent)
            cost += parent[len(parent) - 1]
            parent = child_parent[parent[:-1]]
        result.reverse()
        total_steps = len(result)
        file_stream.write("%d\n" % cost)           # write total cost to output.text
        file_stream.write("%d\n" % total_steps)    # write total number of steps to output.text
        for i in result:
            if i is result[len(result) - 1]:        # last item to be print out without '\n' newline
                for index, each in enumerate(i):
                    if index == len(i) - 1:
                        print(str(each), file=file_stream, end='')
                    else:
                        print(str(each), file=file_stream, end=' ')
            else:
                for index, each in enumerate(i):
                    if index == len(i) - 1:
                        print(str(each), file=file_stream, end='')
                    else:
                        print(str(each), file=file_stream, end=' ')
                print(file=file_stream, end='\n')

    @staticmethod
    def bfs(file_stream, dimension, entrance, exit_gird, action_available):
        COST = 1
        NO_COST = 0
        visited = set()
        child_to_parent = {}
        q = deque()

        # add entrance grid into queue
        q.append(entrance)
        visited.add(entrance)
        child_to_parent[entrance] = None
        while q:
            current_gird = q.popleft()
            if exit_gird in visited:
                exit_gird_with_cost = exit_gird + (COST, )
                Homework1.write_result(file_stream, exit_gird_with_cost, child_to_parent)
                break
            for direction in action_available[current_gird]:
                next_grid = tuple(map(add, current_gird, Homework1._actions[direction + Homework1.NATURAL_NUMBER_TO_INDEX]))
                if next_grid not in visited:
                    q.append(next_grid)
                    if current_gird == entrance:
                        child_to_parent[next_grid] = current_gird + (NO_COST,)
                    else:
                        child_to_parent[next_grid] = current_gird + (COST,)
                    visited.add(next_grid)
        if exit_gird not in child_to_parent:
            Homework1.write_result(file_stream, exit_gird, child_to_parent, fail=True)

    @staticmethod
    def ucs(file_stream, dimension, entrance, exit_gird, action_available):
        STRAITLINE = 10
        DIAGONAL = 14
        straightline_set = (1, 2, 3, 4, 5, 6)
        diagnal_set = (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
        child_parent = {}   # { Gird_object : Grid_object }
        path_cost = {}      # CHANGED { Grid_object : cost } TO { Grid.location : cost }
        explored = set()    # ( Grid.location )
        pq = []             # [ Grid.object ]

        entrance_grid = Homework1.Grid(entrance, 0)
        heapq.heappush(pq, entrance_grid)
        child_parent[entrance_grid] = None
        path_cost[entrance_grid.location] = 0
        while pq:
            # ## data in pq (Grid(location, cost)) ####
            current = heapq.heappop(pq)
            current_loc = current.location
            if current_loc == exit_gird:
                explored.add(current_loc)
                result = deque()
                temp = current
                result.append(tuple(temp.location + (temp.cost,)))
                while child_parent[temp] is not None:
                    result.append(tuple(child_parent[temp].location + (child_parent[temp].cost,)))
                    temp = child_parent[temp]
                result.append(len(result))
                result.append(path_cost[current_loc])
                print(result.pop(), file=file_stream)       # print total cost
                print(result.pop(), file=file_stream)       # print total number of steps
                # print all grids with cost
                for index, item in enumerate(reversed(tuple(result))):
                    if index == len(tuple(result)) - 1:
                        for i, each in enumerate(item):
                            if i == len(item) - 1:
                                print(each, file=file_stream, end='')
                            else:
                                print(each, file=file_stream, end=' ')
                    else:
                        for i, each in enumerate(item):
                            if i == len(item) - 1:
                                print(each, file=file_stream)
                            else:
                                print(each, file=file_stream, end=' ')
                break

            for direction in action_available[current_loc]:
                next_loc = tuple(map(add, current_loc, Homework1._actions[direction + Homework1.NATURAL_NUMBER_TO_INDEX]))
                next_grid = Homework1.Grid(next_loc, None)
                if direction in straightline_set:
                    Homework1.ucs_helper(STRAITLINE, current, next_grid, pq, explored, path_cost, child_parent)
                elif direction in diagnal_set:
                    Homework1.ucs_helper(DIAGONAL, current, next_grid, pq, explored, path_cost, child_parent)

            explored.add(current.location)
        if exit_gird not in explored:
            print('FAIL', file=file_stream, end='')

    @staticmethod
    def ucs_helper(cost, current_grid, next_grid, pq, explored, path_cost, child_parent, test=None):
        if (not(any(grid.location == next_grid.location for grid in pq))) and (next_grid.location not in explored):
            next_grid.cost = cost
            path_cost[next_grid.location] = path_cost[current_grid.location] + cost
            child_parent[next_grid] = current_grid
            heapq.heappush(pq, next_grid)
        elif any(grid.location == next_grid.location for grid in pq):   # next_grid in pq
            if path_cost[next_grid.location] > (path_cost[current_grid.location] + cost):
                for grid in pq:
                    if next_grid.location == grid.location:
                        pq.remove(grid)
                next_grid.cost = cost
                path_cost[next_grid.location] = path_cost[current_grid.location] + cost
                child_parent[next_grid] = current_grid
                heapq.heappush(pq, next_grid)
        elif next_grid.location in explored:
            if path_cost[next_grid.location] > (path_cost[current_grid.location] + cost):
                explored.remove(next_grid.location)
                next_grid.cost = cost
                path_cost[next_grid.location] = path_cost[current_grid.location] + cost
                child_parent[next_grid] = current_grid
                heapq.heappush(pq, next_grid)

    @staticmethod
    def a_star(file_stream, dimension, entrance, exit_gird, action_available):
        STRAITLINE = 10
        DIAGONAL = 14
        straightline_set = (1, 2, 3, 4, 5, 6)
        diagnal_set = (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
        child_parent = {}   # { Gird_object : Grid_object }
        path_cost = {}      # { Grid.location : cost }
        explored = set()    # ( Grid.location )
        pq = []             # [ Grid.object ]

        entrance_grid = Homework1.Grid(entrance, 0)
        heapq.heappush(pq, entrance_grid)
        child_parent[entrance_grid] = None
        path_cost[entrance_grid.location] = 0
        entrance_grid.past_cost = 0
        entrance_grid.heuristic = math.sqrt((entrance[0]-exit_gird[0])**2 + (entrance[1]-exit_gird[1])**2 + (entrance[2]-exit_gird[2])**2)
        while pq:
            # data in pq: Grid(location, cost, heuristic)
            current = heapq.heappop(pq)
            current_loc = current.location
            if current_loc == exit_gird:
                explored.add(current_loc)
                result = deque()
                temp = current
                result.append(tuple(temp.location + (temp.cost,)))
                while child_parent[temp] is not None:
                    result.append(tuple(child_parent[temp].location + (child_parent[temp].cost,)))
                    temp = child_parent[temp]
                result.append(len(result))
                result.append(path_cost[current_loc])
                print(result.pop(), file=file_stream)       # print total cost
                print(result.pop(), file=file_stream)       # print total number of steps
                # print all grids with cost
                for index, item in enumerate(reversed(tuple(result))):
                    if index == len(tuple(result)) - 1:
                        for i, each in enumerate(item):
                            if i == len(item) - 1:
                                print(each, file=file_stream, end='')
                            else:
                                print(each, file=file_stream, end=' ')
                    else:
                        for i, each in enumerate(item):
                            if i == len(item) - 1:
                                print(each, file=file_stream)
                            else:
                                print(each, file=file_stream, end=' ')
                break

            for direction in action_available[current_loc]:
                next_loc = tuple(map(add, current_loc, Homework1._actions[direction + Homework1.NATURAL_NUMBER_TO_INDEX]))
                next_grid = Homework1.Grid(next_loc, None)
                if direction in straightline_set:
                    Homework1.a_star_helper(STRAITLINE, current, next_grid, exit_gird, pq, explored, path_cost, child_parent)
                elif direction in diagnal_set:
                    Homework1.a_star_helper(DIAGONAL, current, next_grid, exit_gird, pq, explored, path_cost, child_parent)

            explored.add(current.location)
        if exit_gird not in explored:
            print('FAIL', file=file_stream, end='')

    @staticmethod
    def a_star_helper(cost, current_grid, next_grid, exit_loc, pq, explored, path_cost, child_parent, test=None):
        next_loc = next_grid.location
        if (not(any(grid.location == next_grid.location for grid in pq))) and (next_grid.location not in explored):
            next_grid.cost = cost
            next_grid.heuristic = math.sqrt((next_loc[0]-exit_loc[0])**2 + (next_loc[1]-exit_loc[1])**2 + (next_loc[2]-exit_loc[2])**2)
            next_grid.past_cost = path_cost[current_grid.location] + cost
            path_cost[next_grid.location] = path_cost[current_grid.location] + cost
            child_parent[next_grid] = current_grid
            heapq.heappush(pq, next_grid)
        elif any(grid.location == next_grid.location for grid in pq):
            if path_cost[next_grid.location] > (path_cost[current_grid.location] + cost):
                for grid in pq:
                    if next_grid.location == grid.location:
                        pq.remove(grid)
                next_grid.cost = cost
                next_grid.past_cost = path_cost[current_grid.location] + cost
                path_cost[next_grid.location] = path_cost[current_grid.location] + cost
                child_parent[next_grid] = current_grid
                heapq.heappush(pq, next_grid)
        elif next_grid.location in explored:
            if path_cost[next_grid.location] > (path_cost[current_grid.location] + cost):
                explored.remove(next_grid.location)
                next_grid.cost = cost
                next_grid.past_cost = path_cost[current_grid.location] + cost
                path_cost[next_grid.location] = path_cost[current_grid.location] + cost
                child_parent[next_grid] = current_grid
                heapq.heappush(pq, next_grid)

# main function below
input_file = open('input.txt', 'r')
algorithm = ''
num_row = 0
entrance = []
dimension = []
exit_gird = []
num_grids_actions = None
locations_actions = {}

for line, content in enumerate(input_file):
    if line == 0:
        algorithm = content.strip()
    elif line == 1:
        # process the data in input file
        dimension = tuple(map(int, content.split()))
    elif line == 2:
        entrance = tuple(map(int, content.split()))
    elif line == 3:
        exit_gird = tuple(map(int, content.split()))
    elif line == 4:
        num_grids_actions = int(content)
    else:
        # store available actions on specific girds to dict. keys are grid in tuple of int
        int_content = tuple(map(int, content.split()))
        locations_actions[int_content[:3]] = int_content[3:]
file_stream = open("output.txt", "w+")
if algorithm == "BFS":
    # print('use bfs!')
    Homework1.bfs(file_stream, dimension, entrance, exit_gird, locations_actions)
elif algorithm == "UCS":
    # print('use UCS!')
    Homework1.ucs(file_stream, dimension, entrance, exit_gird, locations_actions)
elif algorithm == "A*":
    # print('inside A*!')
    Homework1.a_star(file_stream, dimension, entrance, exit_gird, locations_actions)

file_stream.close()
