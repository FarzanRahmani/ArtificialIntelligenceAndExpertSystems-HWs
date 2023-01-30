from Algorithm import Algorithm


class A_STAR(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        #################################################################################
        # "*** YOUR CODE HERE ***"
        self.path = [] 
        self.frontier = [] # queue with priority (f)
        self.explored_set = []

        init_state, goal_state = self.get_initstate_and_goalstate(snake) # start state , goal state

        init_state.g = 0 # cost from root to this node
        init_state.h = self.manhattan_distance(init_state, goal_state) # heuristic cost from this node to goal
        init_state.f = init_state.g + init_state.h
        
        self.frontier.append(init_state) # queue with priority (f) 
        # (better implementation for frontier is with min heap(priority queue))

        while self.frontier:
            node = min(self.frontier, key = lambda n: n.f)
            self.frontier.remove(node)

            if node.equal(goal_state): # reach goal?
                return self.get_path(node)
            
            self.explored_set.append(node)

            for neighbor in self.get_neighbors(node):
                if (neighbor not in self.frontier) and (neighbor not in self.explored_set) and (not self.outside_boundary(neighbor)) and (not self.inside_body(snake, neighbor)):
                    neighbor.parent = node

                    neighbor.g = node.g + 1 # edges costs 1 ### cost from root to this node
                    neighbor.h = self.manhattan_distance(neighbor, goal_state) # heuristic cost from this node to goal
                    neighbor.f = neighbor.g + neighbor.h

                    self.frontier.append(neighbor)
        #################################################################################
        return None
