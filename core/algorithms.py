from utils.constants import Order, Heuristics, Algorithms


class Solution:
    def __init__(self, state, nodes_expanded, max_search_depth):
        self.state = state
        self.nodes_expanded = nodes_expanded
        self.max_search_depth = max_search_depth


def bfs(init):
    import queue

    frontier = queue.Queue()
    frontier.put(init)
    frontier_config = {tuple(init.config): True}
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while not frontier.empty():
        state = frontier.get()
        state.summary()

        explored.add(state.config)
        if state.is_goal():
            return Solution(state, nodes_expanded, max_search_depth)

        nodes_expanded += 1
        for neighbor in state.expand(RLDU=False):
            if neighbor.config not in explored and tuple(neighbor.config) not in frontier_config:
                frontier.put(neighbor)
                frontier_config[tuple(neighbor.config)] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
    return None


def dfs(init):
    import queue

    frontier = queue.LifoQueue()
    frontier.put(init)
    frontier_config = {tuple(init.config): True}
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while not frontier.empty():
        state = frontier.get()
        state.summary()

        explored.add(state.config)
        if state.is_goal():
            return Solution(state, nodes_expanded, max_search_depth)

        nodes_expanded += 1
        for neighbor in state.expand():
            if neighbor.config not in explored and tuple(neighbor.config) not in frontier_config:
                frontier.put(neighbor)
                frontier_config[tuple(neighbor.config)] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
    return None


def a_star(init, order: Order = Order.MIN, heuristic=Heuristics.EUC):
    from core.priority_queue import PriorityQueue

    frontier = PriorityQueue(order, heuristic)
    frontier.append(init)
    frontier_config = {tuple(init.config): True}
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while not frontier.empty():
        state = frontier.pop()
        state.summary()

        explored.add(state)
        if state.is_goal():
            return Solution(state, nodes_expanded, max_search_depth)

        nodes_expanded += 1
        for neighbor in state.expand(RLDU=False):
            if neighbor not in explored and tuple(neighbor.config) not in frontier_config:
                frontier.append(neighbor)
                frontier_config[tuple(neighbor.config)] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
            elif neighbor in frontier:
                if heuristic(neighbor) < frontier[neighbor]:
                    frontier.__delitem__(neighbor)
                    frontier.append(neighbor)
    return None


def solve(init, algorithm: Algorithms, order: Order = None, heuristic=None):
    if algorithm == Algorithms.BFS:
        return bfs(init)
    if algorithm == Algorithms.DFS:
        return dfs(init)
    if algorithm == Algorithms.A_STAR:
        return a_star(init, order, heuristic)
    raise NotImplementedError('[ERROR] No such algorithm is supported.')
