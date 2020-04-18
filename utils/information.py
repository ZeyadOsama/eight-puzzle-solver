from core.algorithms import Solution


class Information(object):
    def __init__(self, solution: Solution, running_time, ram_usage):
        self.solution = solution
        self.running_time = running_time
        self.ram_usage = ram_usage

    def summary(self, verbose=False):
        final_state = self.solution.state

        path_to_goal = [final_state.move]
        parent_state = final_state.parent

        while parent_state:
            if parent_state.parent:
                path_to_goal.append(parent_state.move)
            parent_state = parent_state.parent
        path_to_goal.reverse()

        from utils.constants import RESULT
        print(RESULT)
        print('path_to_goal:')
        print(f'{self.path_to_goal()}\n')

        if verbose:
            print(f'cost_of_path: {str(final_state.cost)}\n')
            print(f'nodes_expanded: {str(self.solution.nodes_expanded)}\n')
            print(f'search_depth: {str(len(path_to_goal))}\n')
            print(f'max_search_depth: {str(self.solution.max_search_depth)}\n')
            print(f'running_time: {str(self.running_time)}\n')
            print(f'max_ram_usage:  {str(self.ram_usage)}\n')

    def path_to_goal(self) -> str:
        path_to_goal = [self.solution.state.move]
        parent_state = self.solution.state.parent

        while parent_state:
            if parent_state.parent:
                path_to_goal.append(parent_state.move)
            parent_state = parent_state.parent
        path_to_goal.reverse()

        path_to_goal_str = ""
        for s in path_to_goal:
            path_to_goal_str += '-> ' + s + ' '
        return path_to_goal_str
