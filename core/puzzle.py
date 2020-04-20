import math
import resource
import time

import utils.constants as c
from core.algorithms import solve
from core.common import Point
from core.heuristics import manhattan, euclidean
from utils.information import Information


class PuzzleState:
    def __init__(self, config, n, goal, cost_function, parent=None, move='Initial', cost=0):
        if n * n != len(config) or n < 2:
            raise AttributeError(f'Length of config entered is not correct or less than required!')
        self.n = n
        self.cost = cost
        self.parent = parent
        self.move = move
        self.dimension = n
        self.config = config
        self.children = []
        self.goal = goal
        self.cost_function = cost_function

        for i, item in enumerate(self.config):
            if item == 0:
                self.empty = Point(x=i // self.n, y=i % self.n)
                break

    def summary(self):
        print(c.STATE_TITLE)
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def expand(self, RLDU=True):
        if len(self.children) == 0:
            # RLDU
            if RLDU:
                right_child = self.__move_right()
                if right_child is not None:
                    self.children.append(right_child)
                left_child = self.__move_left()
                if left_child is not None:
                    self.children.append(left_child)
                down_child = self.__move_down()
                if down_child is not None:
                    self.children.append(down_child)
                up_child = self.__move_up()
                if up_child is not None:
                    self.children.append(up_child)
            # UDLR
            else:
                up_child = self.__move_up()
                if up_child is not None:
                    self.children.append(up_child)
                down_child = self.__move_down()
                if down_child is not None:
                    self.children.append(down_child)
                left_child = self.__move_left()
                if left_child is not None:
                    self.children.append(left_child)
                right_child = self.__move_right()
                if right_child is not None:
                    self.children.append(right_child)
        return self.children

    def __move_up(self):
        if self.empty.x == 0:
            return None
        blank_index = self.empty.x * self.n + self.empty.y
        target = blank_index - self.n
        new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function,
                           parent=self,
                           move=c.Move.RIGHT,
                           cost=self.cost + 1)

    def __move_down(self):
        if self.empty.x == self.n - 1:
            return None
        blank_index = self.empty.x * self.n + self.empty.y
        target = blank_index + self.n
        new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function,
                           parent=self,
                           move=c.Move.DOWN,
                           cost=self.cost + 1)

    def __move_right(self):
        if self.empty.y == self.n - 1:
            return None
        blank_index = self.empty.x * self.n + self.empty.y
        target = blank_index + 1
        new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function,
                           parent=self,
                           move=c.Move.RIGHT,
                           cost=self.cost + 1)

    def __move_left(self):
        if self.empty.y == 0:
            return None
        blank_index = self.empty.x * self.n + self.empty.y
        target = blank_index - 1
        new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function,
                           parent=self,
                           move=c.Move.LEFT,
                           cost=self.cost + 1)

    def is_solvable(self):
        inversion = 0
        for i in range(len(self.config)):
            for j in range(i + 1, len(self.config)):
                if (self.config[i] > self.config[j]) and self.config[i] != 0 and self.config[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

    def is_goal(self):
        return list(self.config) == self.goal

    def __lt__(self, other):
        return self.cost_function(self) < self.cost_function(other)

    def __le__(self, other):
        return self.cost_function(self) <= self.cost_function(other)


class PuzzleSolver:
    def __init__(self, algorithm, init_state, goal_state=c.GOAL_STATE, order=c.Order.MIN,
                 heuristic: c.Heuristics = None):
        self.init_state = init_state
        self.algorithm = algorithm
        self.order = order

        # Create heuristic in A* case.
        if algorithm == c.Algorithms.A_STAR and heuristic is None:
            raise AttributeError(f'Required attribute \'heuristic\' in case of using A* Search.')
        elif heuristic == c.Heuristics.MAN:
            self.heuristic = manhattan
        elif heuristic == c.Heuristics.EUC:
            self.heuristic = euclidean

        # Create a Puzzle State Object with the inputs for Solver.
        init_state = tuple(map(int, init_state))
        size = int(math.sqrt(len(init_state)))
        self.puzzle_state = PuzzleState(init_state, size, goal_state, self.__calculate_total_cost)

        # Start off by checking if state is solvable.
        if not self.puzzle_state.is_solvable():
            raise Exception(f'The initial state entered is not solvable.')

    def solve(self) -> Information:
        mem_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        time_start = time.time()

        solution = solve(self.puzzle_state, self.algorithm, self.order, self.__calculate_total_cost)

        time_end = time.time()
        mem_end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        return Information(solution, time_end - time_start, (mem_end - mem_start) / 1024)

    def __calculate_total_cost(self, state):
        """
        Calculate the total estimated cost of a state.
        """
        sum_heuristic = 0
        for i, item in enumerate(state.config):
            current_point = Point(x=i // state.n, y=i % state.n)
            goal_idx = state.goal.index(item)
            goal_point = Point(x=goal_idx // state.n, y=goal_idx % state.n)
            sum_heuristic += self.heuristic(current_point, goal_point)
        return sum_heuristic + state.cost
