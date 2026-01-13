from Envoirments.aux_funcs import coords_to_key, calc_distance

class LightSensor:
    def __init__(self):
        self.last_light = 0
        pass
    def get_sensor_data(self, all_obs:dict):
        light = all_obs["light_intensity"]
        last_light = self.last_light
        self.last_light = light
        return [last_light, light]

class LaserSensor:
    def __init__(self, max_distance:int):
        self.max_distance = max_distance

    def _aux_get_closest_wall(self, direction:tuple ,items_dict:dict, current_coordinates:tuple, map_size:int):   # (left/right, up/down) - 0, 1 or -1
        output = -2
        local_coordinates = [-1, -1]

        for x_aux in range(self.max_distance):
            local_coordinates[0] = current_coordinates[0] + direction[0]*(x_aux + 1)
            local_coordinates[1] = current_coordinates[1] + direction[1]*(x_aux + 1)
            key_coords = coords_to_key(local_coordinates[0], local_coordinates[1])

            if key_coords in items_dict:
                if items_dict[key_coords].name == "Wall":
                    wall_distance = calc_distance(current_coordinates[0], current_coordinates[1], local_coordinates[0], local_coordinates[1])
                    output = wall_distance
                    break  # only the closest wall matter

        if output == -2: # no wall found
            if local_coordinates[0] < 0 or local_coordinates[1] < 0 or local_coordinates[0] > map_size or local_coordinates[1] > map_size:
                output = -1 # out of map
            else:
                output = 0 # nothing detected

        return output

    def get_sensor_data(self, all_obs:dict):
        current_coordinates = all_obs["agent_pos"]
        items_dict = all_obs["items_dict"]
        map_size = all_obs["env_size"][0]

        output_walls = [0, 0, 0, 0, 0, 0, 0, 0]
        closest_wall_distance = -1

        # left
        direction = (-1, 0)
        closest_wall_distance = self._aux_get_closest_wall(direction=direction, items_dict=items_dict, current_coordinates=current_coordinates, map_size=map_size)
        if closest_wall_distance != -1:
            output_walls[0] = closest_wall_distance / self.max_distance # make the value between 0 and 1

        # right
        direction = (1, 0)
        closest_wall_distance = self._aux_get_closest_wall(direction=direction, items_dict=items_dict, current_coordinates=current_coordinates, map_size=map_size)
        if closest_wall_distance != -1:
            output_walls[1] = closest_wall_distance / self.max_distance  # make the value between 0 and 1

        # up
        direction = (0, -1)
        closest_wall_distance = self._aux_get_closest_wall(direction=direction, items_dict=items_dict, current_coordinates=current_coordinates, map_size=map_size)
        if closest_wall_distance != -1:
            output_walls[2] = closest_wall_distance / self.max_distance  # make the value between 0 and 1

        # down
        direction = (0, 1)
        closest_wall_distance = self._aux_get_closest_wall(direction=direction, items_dict=items_dict, current_coordinates=current_coordinates, map_size=map_size)
        if closest_wall_distance != -1:
            output_walls[3] = closest_wall_distance / self.max_distance  # make the value between 0 and 1

        # up/left
        direction = (-1, -1)
        closest_wall_distance = self._aux_get_closest_wall(direction=direction, items_dict=items_dict, current_coordinates=current_coordinates, map_size=map_size)
        if closest_wall_distance != -1:
            output_walls[4] = closest_wall_distance / self.max_distance  # make the value between 0 and 1

        # up/right
        direction = (1, -1)
        closest_wall_distance = self._aux_get_closest_wall(direction=direction, items_dict=items_dict, current_coordinates=current_coordinates, map_size=map_size)
        if closest_wall_distance != -1:
            output_walls[5] = closest_wall_distance / self.max_distance  # make the value between 0 and 1

        # down/left
        direction = (-1, 1)
        closest_wall_distance = self._aux_get_closest_wall(direction=direction, items_dict=items_dict, current_coordinates=current_coordinates, map_size=map_size)
        if closest_wall_distance != -1:
            output_walls[6] = closest_wall_distance / self.max_distance  # make the value between 0 and 1

        # down/right
        direction = (1, 1)
        closest_wall_distance = self._aux_get_closest_wall(direction=direction, items_dict=items_dict, current_coordinates=current_coordinates, map_size=map_size)
        if closest_wall_distance != -1:
            output_walls[7] = closest_wall_distance / self.max_distance  # make the value between 0 and 1

        return output_walls


class WallSensor:
    def __init__(self, max_distance:int):
        self.max_distance = max_distance

    def get_sensor_data(self, all_obs:dict):
        current_coordinates = all_obs["agent_pos"]
        env_size = all_obs["env_size"]
        items_dict = all_obs["items_dict"]

        walls_output_raw = []
        for xi in range(2*self.max_distance+1):
            for yi in range(2*self.max_distance+1):
                if xi == 0 and yi == 0:
                    continue
                else:
                    local_coords = (current_coordinates[0]+xi-self.max_distance, current_coordinates[1]+yi-self.max_distance)
                    key_coord = coords_to_key(local_coords[0], local_coords[1])
                    if key_coord in items_dict:
                        if items_dict[key_coord].name == "Wall":
                            walls_output_raw.append(1)
                        else:
                            walls_output_raw.append(0)
                    elif local_coords[0] < 0 or local_coords[1] < 0:
                        walls_output_raw.append(-1) # end of the world
                    elif local_coords[0] > env_size[0] or local_coords[1] > env_size[1]:
                        walls_output_raw.append(-1)  # end of the world
                    else:
                        walls_output_raw.append(0)

        return tuple(walls_output_raw)

class DirectionSensor:
    def __init__(self, reference_name:str):
        self.reference_name = reference_name

    def get_sensor_data(self, all_obs:dict):
        current_coordinates = all_obs["agent_pos"]
        reference_coordinates = all_obs[self.reference_name]
        output = [0, 0]

        # X axis
        if current_coordinates[0] < reference_coordinates[0]:
            output[0] = 1
        elif current_coordinates[0] > reference_coordinates[0]:
            output[0] = -1

        # Y axis
        if current_coordinates[1] < reference_coordinates[1]:
            output[1] = 1
        elif current_coordinates[1] > reference_coordinates[1]:
            output[1] = -1

        return output


class Sensor:
    def __init__(self, raw_sensor):
        self.raw_sensor = raw_sensor

    def get_sensor_data(self, all_obs:dict):
        return self.raw_sensor.get_sensor_data(all_obs)
    