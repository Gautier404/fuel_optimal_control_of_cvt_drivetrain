"""This file contains the setup and solution of the optimal control problem as described in the project report."""
import numpy as np
from dynamics_functions import *
from input_data import *
import plotly.graph_objects as go
from gekko import GEKKO

# define boundary conditions such that the vehicle accelerates from 40 kph to 80 kph in 10 seconds:

cvt_ratio_0 = 1.0
cvt_ratio_f = 1.0

t_0 = 0.0
t_f = 20.0

engine_rps_0 = 2000.0/60 
engine_rps_f = 2100.0/60

fuel_used_grams_0 = 0.0 # fuel_used_g_f free

distance_traveled_m_0 = 0.0 # distance_traveled_m_f free

# define input and state bounds

# load pedal
u1_min = 0.0
u1_max = 1.0

# cvt ratio rate of change
u2_min = -1.0
u2_max = 1.0

# cvt ratio
cvt_ratio_min = 0.5
cvt_ratio_max = 10.0


# initialize gekko model
m = GEKKO(remote=False)
n = 101
m.time = np.linspace(0,t_f,n)

# define state variables
cvt_ratio = m.Var(value=cvt_ratio_0, lb=cvt_ratio_min, ub=cvt_ratio_max, name='cvt_ratio')
#m.fix_final(cvt_ratio, val=cvt_ratio_f)
engine_rps = m.Var(value=engine_rps_0, lb=engine_speed_map_rpm.min()/60, ub=engine_speed_map_rpm.max()/60, name='engine_rps')
#m.fix_final(engine_rps, val=engine_rps_f)
fuel_used_grams = m.Var(value=fuel_used_grams_0, lb=0, name='fuel_used_grams')
distance_traveled_m = m.Var(value=distance_traveled_m_0, lb=0, name='distance_traveled_m')

# define input variables
u1 = m.MV(lb=u1_min, ub=u1_max)
u2 = m.MV(lb=u2_min, ub=u2_max)

# define intermediate variables
vehicle_velocity = m.Intermediate(get_vehicle_velocity(cvt_ratio, engine_rps))
def placeholder(engine_rps, u1):
    return engine_rps*u1+50
engine_torque = m.Intermediate(placeholder(engine_rps, u1))## m.Intermediate(get_engine_torque(engine_rps*60, u1))

# define dynamics equations
m.Equation(cvt_ratio.dt() == u2)
m.Equation(engine_rps.dt() == get_engine_rps_derivative(engine_torque, engine_rps, cvt_ratio, u2))
m.Equation(fuel_used_grams.dt() == get_fuel_consumption(engine_torque, engine_rps))
m.Equation(distance_traveled_m.dt() == vehicle_velocity)

# define cost function and objective
# J = m.Var(value=0) # objective (profit)
# Jf = m.FV() # final objective
# Jf.STATUS = 1
# m.Connection(Jf,J,pos2='end')
# m.Equation(J.dt() == fuel_used_grams/distance_traveled_m)
m.Minimize(fuel_used_grams/distance_traveled_m) # minimize fuel used per distance traveled

# define solver options
m.options.IMODE = 6  # optimal control
m.options.NODES = 3  # collocation nodes
m.options.SOLVER = 3 # solver (IPOPT)
m.options.COLDSTART = 2 # coldstart on first solve

m.open_folder()
m.solve(disp=True) # Solve

print(engine_rps.value)
# plot results
fig = go.Figure()
fig.add_trace(go.Scatter(x=m.time, y=cvt_ratio.value, mode='lines', name='cvt_ratio'))
fig.add_trace(go.Scatter(x=m.time, y=engine_rps.value, mode='lines', name='engine_rps'))
fig.add_trace(go.Scatter(x=m.time, y=60*np.array(engine_rps.value), mode='lines', name='engine rpm'))
fig.add_trace(go.Scatter(x=m.time, y=fuel_used_grams.value, mode='lines', name='fuel used'))
fig.add_trace(go.Scatter(x=m.time, y=distance_traveled_m.value, mode='lines', name='distance traveled'))
fig.add_trace(go.Scatter(x=m.time, y=u1.value, mode='lines', name='load pedal'))
fig.add_trace(go.Scatter(x=m.time, y=u2.value, mode='lines', name='cvt ratio rate of change'))
fig.add_trace(go.Scatter(x=m.time, y=vehicle_velocity.value, mode='lines', name='vehicle velocity'))
fig.add_trace(go.Scatter(x=m.time, y=engine_torque.value, mode='lines', name='engine torque'))
fig.update_layout(title = 'states over time', xaxis_title='time, s')
fig.show()

# ask whether to save the plot
save_plot = input("Save plot? (y/n): ")
if save_plot == 'y':
    fig.write_html("./graphs/states_over_time.html")





