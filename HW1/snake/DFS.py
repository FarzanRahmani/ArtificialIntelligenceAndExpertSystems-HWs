from Utility import Node
from Algorithm import Algorithm

# import sys
# sys.setrecursionlimit(200000)

class DFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        
        # این باعث میشه تو یه لوپ نیفته اگه مسیر پر بود از قبل همونو ریترن کنه اگه نه دوباره صفرش کنه الگوریتم رو طی کنه
        if len(self.path) != 0:
            path = self.path.pop()
            if not self.inside_body(snake, path):
                return path
                
        self.path = []
        self.frontier = []
        self.explored_set = []
        init_state, goal_state = self.get_initstate_and_goalstate(snake)
        self.frontier.append(init_state) # stack
        
        while self.frontier:
            node = self.frontier.pop()
            if node.equal(goal_state):
                # self.frontier = []
                # self.explored_set = []
                # return node
                return self.get_path(node)
            
            self.explored_set.append(node)

            for neighbor in self.get_neighbors(node):
                if (neighbor not in self.frontier) and (neighbor not in self.explored_set) and (not self.inside_body(snake, neighbor) and (not self.outside_boundary(neighbor))):
                    neighbor.parent = node
                    self.frontier.append(neighbor)
                    # return neighbor
        
        #################################################################################
        # return self.recursive_dfs(snake, init_state, goal_state)

        #################################################################################
        return None

    # def recursive_dfs(self, snake, node, goal_state):
    #     self.explored_set.append(node)
    #     for neighbor in self.get_neighbors(node):
    #         if node.equal(goal_state):
    #             return self.get_path(node)
    #         if (neighbor not in self.explored_set) and (not self.inside_body(snake, neighbor) and (not self.outside_boundary(neighbor))):
    #             neighbor.parent = node
    #             return self.recursive_dfs(snake, node, goal_state)
