"""This file contains functions for easily graphing certain figures that can be used throughout this project."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_throttle_rpm_torque_map(engine_torque_map_Nm, engine_speed_map_rpm, engine_throttle_map):
    torque_map_fig = go.Figure(data=[go.Surface(z=engine_torque_map_Nm, x=engine_throttle_map, y=engine_speed_map_rpm)])
    torque_map_fig.update_layout(title='torque, rpm, throttle map', xaxis_title='throttle, %', yaxis_title='rpm')
    torque_map_fig.show()

def plot_throttle_rpm_power_map(engine_power_map_W, engine_speed_map_rpm, engine_throttle_map):
    power_map_fig = go.Figure(data=[go.Surface(z=engine_power_map_W, x=engine_throttle_map, y=engine_speed_map_rpm)])
    power_map_fig.update_layout(title = 'power, rpm, throttle map', xaxis_title='throttle, %', yaxis_title='rpm')
    power_map_fig.show()

def plot_torque_rpm_fuel_consumption_map(engine_fuel_consumption_map_g_s, torque_linspace, rpm_linspace):
    fuel_consumption_map_fig = go.Figure(data=[go.Surface(z=engine_fuel_consumption_map_g_s, x=torque_linspace, y=rpm_linspace)])
    fuel_consumption_map_fig.update_layout(title = 'fuel consumption, rpm, torque map', xaxis_title='torque, Nm', yaxis_title='rpm')
    fuel_consumption_map_fig.show()

def plot_power_torque_rpm_curve(engine_power_map_W, engine_torque_map_Nm, engine_speed_map_rpm):
    power_torque_curve_fig = make_subplots(specs=[[{"secondary_y": True}]])
    power_torque_curve_fig.add_trace(go.Scatter(x=engine_speed_map_rpm, y=engine_power_map_W[:,-1]/1000, mode='lines', name='power'), secondary_y=True)
    power_torque_curve_fig.add_trace(go.Scatter(x=engine_speed_map_rpm, y=engine_torque_map_Nm[:,-1], mode='lines', name='torque'), secondary_y=False)
    power_torque_curve_fig.update_layout(title = 'power, torque, rpm curve', xaxis_title='rpm')
    power_torque_curve_fig.update_yaxes(title_text="power, kW", secondary_y=False)
    power_torque_curve_fig.update_yaxes(title_text="torque, Nm", secondary_y=True)
    power_torque_curve_fig.show()