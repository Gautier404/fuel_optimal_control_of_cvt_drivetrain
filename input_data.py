import numpy as np

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

engine_power_map_W = engine_torque_map_Nm * engine_speed_map_rpm[:, None] / 60

max_torque = np.max(engine_torque_map_Nm)
resolution = 100
torque_linspace = np.linspace(0, max_torque, resolution)
rpm_linspace = np.linspace(np.min(engine_torque_map_Nm), np.max(engine_torque_map_Nm), resolution)
engine_fuel_consumption_map_g_s = torque_linspace @ rpm_linspace
print(engine_fuel_consumption_map_g_s)

if __name__ == '__main__':
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # throttle & rpm -> torque map
    torque_map_fig = go.Figure(data=[go.Surface(z=engine_torque_map_Nm, x=engine_throttle_map, y=engine_speed_map_rpm)])
    torque_map_fig.update_layout(title='torque, rpm, throttle map', xaxis_title='throttle, %', yaxis_title='rpm')
    torque_map_fig.show()

    # throttle & rpm -> power map
    power_map_fig = go.Figure(data=[go.Surface(z=engine_power_map_W, x=engine_throttle_map, y=engine_speed_map_rpm)])
    power_map_fig.update_layout(title = 'power, rpm, throttle map', xaxis_title='throttle, %', yaxis_title='rpm')
    power_map_fig.show()

    # torque & rpm -> fuel consumption map
    fuel_consumption_map_fig = go.Figure(data=[go.Surface(z=engine_fuel_consumption_map_g_s, x=torque_linspace, y=rpm_linspace)])
    fuel_consumption_map_fig.update_layout(title = 'fuel consumption, rpm, torque map', xaxis_title='torque, Nm', yaxis_title='rpm')
    fuel_consumption_map_fig.show()

    # power, torque, rpm curve
    power_torque_curve_fig = make_subplots(specs=[[{"secondary_y": True}]])
    power_torque_curve_fig.add_trace(go.Scatter(x=engine_speed_map_rpm, y=engine_power_map_W[:,-1]/1000, mode='lines', name='power'), secondary_y=True)
    power_torque_curve_fig.add_trace(go.Scatter(x=engine_speed_map_rpm, y=engine_torque_map_Nm[:,-1], mode='lines', name='torque'), secondary_y=False)
    power_torque_curve_fig.update_layout(title = 'power, torque, rpm curve', xaxis_title='rpm')
    power_torque_curve_fig.update_yaxes(title_text="power, kW", secondary_y=False)
    power_torque_curve_fig.update_yaxes(title_text="torque, Nm", secondary_y=True)
    power_torque_curve_fig.show()
