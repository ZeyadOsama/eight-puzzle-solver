STATE_TITLE = '\n' + ('*' * 10) + ' Current State ' + ('*' * 10)
RESULT = '\n' + ('*' * 10) + ' Result ' + ('*' * 10) + '\n'

GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]


class Heuristics:
    MAN = 'manhattan'
    EUC = 'euclidean'


class Algorithms:
    BFS = 'bfs'
    DFS = 'dfs'
    A_STAR = 'astar'


class Order:
    MIN = 'min'
    MAX = 'max'


class Move:
    RIGHT = 'Right'
    LEFT = 'Left'
    UP = 'Up'
    DOWN = 'Down'


class Terminal(str):
    ANSI_RESET = '\u001B[0m'
    ANSI_RED = '\u001B[31m'
    ANSI_GREEN = '\u001B[32m'


def error(msg: str) -> str:
    return f'{Terminal.ANSI_RED}[ERROR] {msg}{Terminal.ANSI_RESET}'


def success(msg: str) -> str:
    return f'{Terminal.ANSI_RED}[SUCCESS] {msg}{Terminal.ANSI_RESET}'


def print_error(msg: str):
    print(error(msg))


def print_success(msg: str):
    print(success(msg))
