import numpy as np
from figures import plot_throttle_rpm_torque_map, plot_throttle_rpm_power_map, plot_torque_rpm_fuel_consumption_map, plot_power_torque_rpm_curve

engine_torque_map_Nm = np.array(
                        [[45,	90,	107, 109, 110, 111,	114, 116],
                        [60, 105, 132, 133, 134, 136, 138, 141],
                        [35, 89, 133, 141, 142, 144, 145, 149],
                        [19, 70, 133, 147, 148, 150, 151, 155],
                        [3, 55, 133, 153, 159, 161, 163, 165],
                        [0, 41, 126, 152, 161, 165, 167, 171],
                        [0, 33, 116, 150, 160, 167, 170, 175],
                        [0, 26, 110, 155, 169, 176, 180, 184],
                        [0, 18, 106, 155, 174, 179, 185, 190],
                        [0, 12, 96, 147, 167, 175, 181, 187],
                        [0, 4, 84, 136, 161, 170, 175, 183],
                        [0, 0, 72, 120, 145, 153, 159, 171]])
engine_speed_map_rpm = np.array([800, 1300, 1800, 2300, 2800, 3300, 3800, 4300, 4800, 5300, 5800, 6300])
engine_throttle_map = [5, 10, 20, 30, 40, 50, 60, 100]

engine_throttle_grid, engine_rpm_grid = np.meshgrid(engine_throttle_map, engine_speed_map_rpm, indexing='ij')

engine_power_map_W = engine_torque_map_Nm * engine_speed_map_rpm[:, None] / 60



def get_engine_fuel_consumption_gps(engine_torque_Nm, engine_speed_rpm):
    """Returns engine fuel consumption in grams/s"""
    FUEL_CONSUMPTION_CONST = 0.001
    return engine_torque_Nm * engine_speed_rpm * FUEL_CONSUMPTION_CONST


resolution = 100
torque_linspace = np.linspace(0, np.max(engine_torque_map_Nm), resolution)
rpm_linspace = np.linspace(np.min(engine_speed_map_rpm), np.max(engine_speed_map_rpm), resolution)
engine_fuel_consumption_map_g_s = np.zeros((resolution, resolution))
for i, torque in enumerate(torque_linspace):
    for j, rpm in enumerate(rpm_linspace):
        engine_fuel_consumption_map_g_s[i, j] = get_engine_fuel_consumption_gps(torque, rpm)

# create program that creates a function that interpolates the engine torque map without using scipy


if __name__ == '__main__':
    plot_throttle_rpm_torque_map(engine_torque_map_Nm, engine_speed_map_rpm, engine_throttle_map)
    plot_throttle_rpm_power_map(engine_power_map_W, engine_speed_map_rpm, engine_throttle_map)
    plot_torque_rpm_fuel_consumption_map(engine_fuel_consumption_map_g_s, torque_linspace, rpm_linspace)
    plot_power_torque_rpm_curve(engine_power_map_W, engine_torque_map_Nm, engine_speed_map_rpm)