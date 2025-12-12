
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

