from core.heuristics import *
from core.algorithms import bfs, dfs, a_star
from utils.information import Information
import utils.constants as c
import time
import resource
import math


class PuzzleState(object):
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
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function,
                               parent=self,
                               move=c.Move.LEFT,
                               cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function,
                               parent=self,
                               move=c.Move.RIGHT,
                               cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function,
                               parent=self,
                               move=c.Move.RIGHT,
                               cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function,
                               parent=self,
                               move=c.Move.DOWN,
                               cost=self.cost + 1)

    def expand(self, RLDU=True):
        if len(self.children) == 0:
            if RLDU:  # RLDU
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
            else:  # UDLR
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
        return self.children

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


class PuzzleSolver(object):
    def __init__(self, initial_state, goal, algorithm=c.Algorithms.BFS, order=c.Order.MIN, heuristic=None):
        self.initial_state = initial_state

        # Assign the search algorithm that will be used in the solver.
        if algorithm == c.Algorithms.BFS:
            self.search_alg = bfs
        elif algorithm == c.Algorithms.DFS:
            self.search_alg = dfs
        elif algorithm == c.Algorithms.A_STAR:
            self.search_alg = a_star
        else:
            raise NotImplementedError('No such algorithm is supported.')

        self.order = order

        # Assign the heuristic algorithm that will be used in the solver.
        if heuristic is None and algorithm == c.Algorithms.A_STAR:
            raise AttributeError(f'Required Attribute `heuristic` in case of using A* Search.')
        elif heuristic == c.Heuristics.MAN:
            self.dist_metric = manhattan
        elif heuristic == c.Heuristics.EUC:
            self.dist_metric = euclidean
        elif heuristic is None and algorithm != c.Algorithms.A_STAR:
            pass
        else:
            raise NotImplementedError(c.error('No such Heuristic is supported.'))

        # Create a Puzzle State Object with the inputs for Solver.
        initial_state = tuple(map(int, initial_state))
        size = int(math.sqrt(len(initial_state)))
        self.puzzle_state = PuzzleState(initial_state, size, goal, self.calculate_total_cost)

        # Start off by checking the solvability of the state and raise error in case of false.
        if not self.puzzle_state.is_solvable():
            raise Exception(f'The initial state entered is not solvable.')

    def calculate_total_cost(self, state):
        """
        Calculate the total estimated cost of a state.
        """
        sum_heuristic = 0
        for i, item in enumerate(state.config):
            current_point = Point(x=i // state.n, y=i % state.n)
            goal_idx = state.goal.index(item)
            goal_point = Point(x=goal_idx // state.n, y=goal_idx % state.n)
            sum_heuristic += self.dist_metric(current_point, goal_point)
        return sum_heuristic + state.cost

    def solve(self) -> Information:
        start_time = time.time()
        mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        if self.search_alg == a_star:
            solution = a_star(self.puzzle_state, self.order, self.calculate_total_cost)
        else:
            solution = self.search_alg(self.puzzle_state)

        running_time = time.time() - start_time
        mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        ram_usage = (mem_final - mem_init) / 1024
        return Information(solution, running_time, ram_usage)
