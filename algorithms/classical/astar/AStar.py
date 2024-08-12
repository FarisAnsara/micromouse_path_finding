import heapq
from memory_profiler import profile
from algorithms.utilities import MoveMouse, Utils, Walls


class AStar(Walls, Utils, MoveMouse):
    def __init__(self, walls, maze_width=16, maze_height=16):
        Walls.__init__(self, walls=walls, maze_width=maze_width, maze_height=maze_height)
        MoveMouse.__init__(self)
        self.distances = [[float('inf')] * self.maze_width for _ in range(self.maze_height)]
        self.goal_positions = self.get_goal_position()
        self.directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,
            (1, 0): self.EAST,
            (0, -1): self.SOUTH,
            (-1, 0): self.WEST
        }

    def heuristic(self, pos):
        gx, gy = self.goal_positions[0]
        return abs(pos[0] - gx) + abs(pos[1] - gy)

    def a_star(self):
        pq = [(self.heuristic(self.start_position), 0, self.start_position)]
        self.distances[self.start_position[0]][self.start_position[1]] = 0

        while pq:
            priority, current_distance, position = heapq.heappop(pq)
            x, y = position

            if position in self.goal_positions:
                break

            if current_distance > self.distances[x][y]:
                continue

            for direction in self.directions:
                dx, dy = self.directionVectors[direction]
                neighbor = (x + dx, y + dy)

                if (0 <= neighbor[0] < self.maze_width and 0 <= neighbor[1] < self.maze_height
                        and not self.wall_between(position, direction)):
                    new_distance = current_distance + 1

                    if new_distance < self.distances[neighbor[0]][neighbor[1]]:
                        self.distances[neighbor[0]][neighbor[1]] = new_distance
                        priority = new_distance + self.heuristic(neighbor)
                        heapq.heappush(pq, (priority, new_distance, neighbor))

    @profile
    def find_shortest_path_to_goal(self):
        self.a_star()
        goal_position = min(self.goal_positions, key=lambda pos: self.distances[pos[0]][pos[1]])
        self.curr_position = goal_position
        self.path.append(self.curr_position)

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