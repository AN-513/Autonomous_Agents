from Envoirments.aux_funcs import coords_to_key

class LightSensor:
    def __init__(self):
        self.last_light = 0
        pass
    def get_sensor_data(self, all_obs:dict):
        light = all_obs["light_intensity"]
        last_light = self.last_light
        self.last_light = light
        return [last_light, light]

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
    