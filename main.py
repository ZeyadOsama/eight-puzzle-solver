import sys

import utils.constants as c
from core.puzzle import PuzzleSolver


def print_help():
    import textwrap as tw
    print('About:')
    print(
        tw.indent(tw.fill(
            'Given a 3×3 board with 8 tiles (every tile has one number from 1 to 8)'
            'and one empty space. The objective is to place the numbers on tiles '
            'to match final configuration using the empty space. We can slide four adjacent '
            '(left, right, above and below) tiles into the empty space.'),
            '\t\t'))
    print('\nUsage:')
    print(tw.indent('python3 puzzle.py -p <order> -a <algorithm> [options]', '\t\t'))

    print('\nOptions:')
    print(tw.indent('-v\t\tVerbose Mode.', '\t\t'))


def get_args():
    if len(sys.argv) < 2:
        print_help()
        exit(-1)

    init_state = None
    algorithm = None
    verbose = False

    for i, arg in enumerate(sys.argv):
        if arg == '-p' or arg == '--puzzle':
            init_state = sys.argv[i + 1].split(',')
        elif arg == '-a' or arg == '--alg':
            algorithm = str(sys.argv[i + 1])
        elif arg == '-v' or arg == '--verbose':
            verbose = True

    if init_state is None or algorithm is None:
        print_help()
        exit(-1)

    return init_state, algorithm, verbose


def get_heuristic(algorithm):
    if algorithm == c.Algorithms.A_STAR:
        value = input('Heuristic is needed for A* algorithm:\n[1] Manhattan\n[2] Euclidean\n')
        if value == str(1):
            return c.Heuristics.MAN
        elif value == str(2):
            return c.Heuristics.EUC
        else:
            c.print_error(f'Heuristic be either -h {c.Heuristics.MAN} or -h {c.Heuristics.EUC}')
            exit(-1)
    return None


def main():
    init_state, algorithm, verbose = get_args()
    heuristic = get_heuristic(algorithm)

    solver = PuzzleSolver(algorithm, init_state=init_state, goal_state=c.GOAL_STATE, heuristic=heuristic)
    solution = solver.solve()
    solution.summary(verbose=True)


if __name__ == '__main__':
    main()
