from algorithms.utilities import MoveMouse, Utils, Walls
from collections import deque


class BFS(Walls, Utils, MoveMouse):

    def __init__(self, walls, maze_width=16, maze_height=16):
        Walls.__init__(self, walls=walls, maze_width=maze_width, maze_height=maze_height)
        MoveMouse.__init__(self)
        inf = self.maze_width * self.maze_height
        self.distances = [[float('inf')] * self.maze_width for _ in range(self.maze_height)]
        self.goal_positions = self.get_goal_position()
        self.directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,  # Moving North
            (1, 0): self.EAST,  # Moving East
            (0, -1): self.SOUTH,  # Moving South
            (-1, 0): self.WEST  # Moving West
        }

    def bfs(self):
        queue = deque([self.start_position])
        visited = set()
        self.distances[self.start_position[0]][self.start_position[1]] = 0
        while queue:
            position = queue.pop()
            visited.add(position)
            x, y = position
            current_distance = self.distances[x][y]

            for direction in self.directions:
                dx, dy = self.directionVectors[direction]
                neighbor = (x + dx, y + dy)

                if (0 <= neighbor[0] < self.maze_width and 0 <= neighbor[1] < self.maze_height
                        and not self.wall_between(position, direction) and neighbor not in visited):
                    queue.appendleft(neighbor)
                    self.distances[neighbor[0]][neighbor[1]] = current_distance + 1

    def find_shortest_path_to_goal(self):
        self.bfs()
        goal_position = min(self.get_goal_position(), key=lambda pos: self.distances[pos[0]][pos[1]])
        self.curr_position = goal_position
        self.path.append(self.curr_position)
        x,y =self.curr_position
        for direction in self.directions:
            dx, dy = self.directionVectors[direction]
            nx, ny = x + dx, y + dy
            if not self.wall_between(self.curr_position, direction) and (nx,ny) not in self.goal_positions:
                self.orientation = direction
                print(self.orientation)

        while self.curr_position != self.start_position:
            x, y = self.curr_position
            neighbors = [(x + dx, y + dy) for dx, dy in self.directionVectors.values()]
            valid_neighbors = [
                pos for pos in neighbors
                if 0 <= pos[0] < self.maze_width and 0 <= pos[1] < self.maze_height and
                   not self.wall_between(self.curr_position, self.directionVectors_inverse[(pos[0] - x, pos[1] - y)])
            ]
            next_position = min(valid_neighbors, key=lambda pos: self.distances[pos[0]][pos[1]])
            direction = self.directionVectors_inverse[(next_position[0] - x, next_position[1] - y)]
            self.move_update_position(direction)

        self.path.reverse()
        return self.path

