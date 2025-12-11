def coords_to_key(x: int, y: int):
    return str(x) + "-" + str(y)


def key_to_coords(key: str):
    raw_numbers = key.split("-")
    numeric_list = []
    for n in raw_numbers:
        numeric_list.append(int(n))
    return numeric_list


def get_relative_direction(agent_x: int, agent_y: int, goal_x: int, goal_y: int):
    direction = [0, 0]

    if goal_x < agent_x:
        direction[0] = -1
    elif goal_x > agent_x:
        direction[0] = 1

    if goal_y < agent_y:
        direction[1] = -1
    elif goal_y > agent_y:
        direction[1] = 1

    return tuple(direction)