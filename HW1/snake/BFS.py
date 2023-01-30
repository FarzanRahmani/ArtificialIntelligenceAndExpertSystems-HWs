from collections import deque
from Utility import Node
from Algorithm import Algorithm


class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        #################################################################################
        # "*** YOUR CODE HERE ***"
        self.frontier = []
        self.explored_set = []
        init_state, goal_state = self.get_initstate_and_goalstate(snake)
        self.frontier.append(init_state) # queue
        
        while self.frontier:
            node = self.frontier.pop(0)
            # if node.x == goal_state.x and node.y == goal_state.y:
            if node.equal(goal_state):
                # self.frontier = []
                # self.explored_set = []
                # return node
                return self.get_path(node)
            
            self.explored_set.append(node)

            for neighbor in self.get_neighbors(node):
                if (neighbor not in self.frontier) and (neighbor not in self.explored_set) and (not self.outside_boundary(neighbor)) and (not self.inside_body(snake, neighbor)):
                    neighbor.parent = node
                    self.frontier.append(neighbor)
                    # return neighbor
        
        #################################################################################
        return None
