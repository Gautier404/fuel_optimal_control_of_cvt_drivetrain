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
t_f = 10.0

engine_rps_0 = 2000.0/60 
engine_rps_f = 4000.0/60

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
cvt_ratio_max = 2.0


# # initialize state arrays
# num_time_steps = 100 # number of time steps
# time_step_s = (t_f - t_0) / num_time_steps # time step size
# t = np.linspace(t_0, t_f, num_time_steps) # time array
# cvt_ratio = np.zeros(num_time_steps) # cvt ratio array
# cvt_ratio[0] = cvt_ratio_0 # initial cvt ratio
# engine_rps = np.zeros(num_time_steps) # engine rpm array
# engine_rps[0] = engine_rps_0 # initial engine rpm
# fuel_used_grams = np.zeros(num_time_steps) # fuel used array
# fuel_used_grams[0] = fuel_used_grams_0 # initial fuel used
# distance_traveled_m = np.zeros(num_time_steps) # distance traveled array
# distance_traveled_m[0] = distance_traveled_m_0 # initial distance traveled

# # initialize intermediate variable arrays
# vehicle_velocity = np.zeros(num_time_steps) # vehicle velocity array in m/s
# engine_torque = np.zeros(num_time_steps) # engine torque array

# # initialize input arrays
# u1 = np.ones(num_time_steps) # load pedal array
# u2 = np.zeros(num_time_steps) # cvt ratio rate of change array


# initialize gekko model
m = GEKKO(remote=False)
n = 101
m.time = np.linspace(0,10,n)

# define state variables
cvt_ratio = m.Var(value=cvt_ratio_0, lb=cvt_ratio_min, ub=cvt_ratio_max)
m.fix_final(cvt_ratio, val=cvt_ratio_f)
engine_rps = m.Var(value=engine_rps_0, lb=engine_speed_map_rpm.min()/60, ub=engine_speed_map_rpm.max()/60)
m.fix_final(engine_rps, val=engine_rps_f)
fuel_used_grams = m.Var(value=fuel_used_grams_0, lb=0)
distance_traveled_m = m.Var(value=distance_traveled_m_0, lb=0)

# define input variables
u1 = m.MV(lb=u1_min, ub=u1_max)
u2 = m.MV(lb=u2_min, ub=u2_max)

# define intermediate variables
vehicle_velocity = m.Intermediate(get_vehicle_velocity(cvt_ratio, engine_rps))
def placeholder(engine_rps, u1):
    return engine_rps*u1
engine_torque = m.Intermediate(placeholder(engine_rps, u1))## m.Intermediate(get_engine_torque(engine_rps*60, u1))

# define dynamics equations
m.Equation(cvt_ratio.dt() == u2)
m.Equation(engine_rps.dt() == get_engine_rps_derivative(engine_torque, engine_rps, cvt_ratio, u2))
m.Equation(fuel_used_grams.dt() == get_fuel_consumption(engine_torque, engine_rps))
m.Equation(distance_traveled_m.dt() == vehicle_velocity)

# define cost function and objective
J = m.Var(value=0) # objective (profit)
Jf = m.FV() # final objective
Jf.STATUS = 1
m.Connection(Jf,J,pos2='end')
m.Equation(J.dt() == fuel_used_grams/distance_traveled_m)
m.Minimize(Jf) # minimize fuel used per distance traveled

# define solver options
m.options.IMODE = 6  # optimal control
m.options.NODES = 3  # collocation nodes
m.options.SOLVER = 3 # solver (IPOPT)
m.solve(disp=True) # Solve

# # integrate forward to get states
# for i in range(1, num_time_steps):
#     engine_torque[i-1] = get_engine_torque(engine_rps[i-1]*60, u1[i-1])
#     vehicle_velocity[i-1] = get_vehicle_velocity(cvt_ratio[i-1], engine_rps[i-1])
#     engine_rps_derivative = get_engine_rps_derivative(engine_torque[i-1], engine_rps[i-1], cvt_ratio[i-1], u2[i-1])
#     fuel_consumption_grams_per_s = get_fuel_consumption(engine_torque[i-1], engine_rps[i-1])

#     # update states
#     cvt_ratio[i] = cvt_ratio[i-1] + u2[i-1] * time_step_s
#     engine_rps[i] = engine_rps[i-1] + engine_rps_derivative * time_step_s
#     fuel_used_grams[i] = fuel_used_grams[i-1] + fuel_consumption_grams_per_s * time_step_s
#     distance_traveled_m[i] = distance_traveled_m[i-1] + vehicle_velocity[i-1] * time_step_s

# engine_torque[num_time_steps-1] = get_engine_torque(engine_rps[num_time_steps-1]*60, u1[num_time_steps-1])
# vehicle_velocity[num_time_steps-1] = get_vehicle_velocity(cvt_ratio[num_time_steps-1], engine_rps[num_time_steps-1])

# # plot results
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=t, y=cvt_ratio, mode='lines', name='cvt ratio'))
# fig.add_trace(go.Scatter(x=t, y=engine_rps*60, mode='lines', name='engine rpm'))
# fig.add_trace(go.Scatter(x=t, y=fuel_used_grams, mode='lines', name='fuel used'))
# fig.add_trace(go.Scatter(x=t, y=distance_traveled_m, mode='lines', name='distance traveled'))
# fig.add_trace(go.Scatter(x=t, y=u1, mode='lines', name='load pedal'))
# fig.add_trace(go.Scatter(x=t, y=u2, mode='lines', name='cvt ratio rate of change'))
# fig.add_trace(go.Scatter(x=t, y=vehicle_velocity, mode='lines', name='vehicle velocity'))
# fig.add_trace(go.Scatter(x=t, y=engine_torque, mode='lines', name='engine torque'))
# fig.update_layout(title = 'states over time', xaxis_title='time, s')
# fig.show()





