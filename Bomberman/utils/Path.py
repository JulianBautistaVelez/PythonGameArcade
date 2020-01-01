from utils.Position import Position


class PathFinder:

    @staticmethod
    def find_path_only_two_directions(grid, starting_pos: Position, end_pos: Position):
        steps = []
        current_pos = starting_pos
        path = grid
        print("TAMAÑO DEL GRID RECIBIDO POR PATHFINDER:")
        print(len(grid))
        print(len(grid[0]))
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in grid]))
        possible_steps = []
        distances = []
        while current_pos != end_pos:
            if path[current_pos.pos_x + 1][current_pos.pos_y] == 0:
                possible_steps.append(Position(current_pos.pos_x + 1, current_pos.pos_y))
            if path[current_pos.pos_x - 1][current_pos.pos_y] == 0:
                possible_steps.append(Position(current_pos.pos_x - 1, current_pos.pos_y))
            if path[current_pos.pos_x][current_pos.pos_y + 1] == 0:
                possible_steps.append(Position(current_pos.pos_x, current_pos.pos_y + 1))
            if path[current_pos.pos_x][current_pos.pos_y - 1] == 0:
                possible_steps.append(Position(current_pos.pos_x, current_pos.pos_y - 1))
            for i in range(len(possible_steps)):
                distances.append(possible_steps[i].distance_to(end_pos))

            if len(possible_steps) == 0:
                if len(steps) > 0:
                    current_pos = steps.pop()
                else:
                    print("NO SE HA ENCONTRADO SOLUCION")
                    break

            else:
                steps.append(possible_steps[distances.index(min(distances))])
                # print("SIGUIENTE PASO")
                # print(possible_steps[distances.index(min(distances))])
                grid[current_pos.pos_x][current_pos.pos_y] = 2
                current_pos = possible_steps[distances.index(min(distances))]
                possible_steps.clear()
                distances.clear()

        # print("MAPA SOLUCIONADO:")
        # print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #                  for row in grid]))
        for i in range(len(steps)):
            print(steps[i])
        return steps