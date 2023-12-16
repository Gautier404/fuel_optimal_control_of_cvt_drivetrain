"""
This file contains the functions that can be used to describe the dynamics of the cvt powertrain system.
These functions are intended to be used in the forward backward algorithm used to solve the optimal
control problem.
"""
from scipy.interpolate import interpn
from input_data import engine_torque_map_Nm, engine_speed_map_rpm, engine_throttle_map
import numpy as np

# Define system constants:
ENGINE_INERTIA = 100.0          # inertia of the engine & driving clutch of the cvt [kg*m^2]
DRIVE_ASSEMBLY_RATIO = 2      # ratio of the drive assembly (speed of wheels/ speed of cvt output)
VEHICLE_INERTIA = 1000.0        # inertia of the vehicle including the wheels and drivetrain [kg*m^2]
WHEEL_RADIUS = 0.25             # radius of the wheels [m]


# Define helper functions for intermediate dynamic variables:
def get_engine_torque(engine_rpm, u1):
    """Compute the engine torque
    
    Arguments:
        engine_rpm (float): engine speed
        u1 (float): engine throttle [0-1]
    """
    # Perform interpolation using interpn
    load_pedal = u1*100
    
    return interpn((engine_speed_map_rpm, engine_throttle_map), engine_torque_map_Nm, [engine_rpm, load_pedal], method='linear')[0]

def get_vehicle_resistive_force(vehicle_velocity):
    """Compute the resistive force of the vehicle due to drag and friction
    
    Arguments:
        vehicle_velocity (float): velocity of the vehicle in meters per second
    """
    a1 = 50
    a2 = 25#100
    return a1 + a2 * vehicle_velocity**2


# state dynmics functions:
def get_cvt_ratio_derivative(u2):
    """Compute the time derivative of the cvt ratio r_cvt
    
    Arguments:
        u2 (float): cvt ratio rate of change
    """
    return u2

def get_vehicle_velocity(cvt_ratio, engine_rps):
    """Compute the vehicle velocity in meters per second
    
    Arguments:
        cvt_ratio (float): cvt ratio
        engine_rpm (float): engine speed
    """
    return engine_rps * cvt_ratio * DRIVE_ASSEMBLY_RATIO * WHEEL_RADIUS

def get_engine_rps_derivative(engine_torque, engine_rps, cvt_ratio, u2):
    """Compute the time derivative of the engine speed
    
    Arguments:
        engine_torque (float): engine torque [Nm]
        engine_rpm (float): engine speed [rps]
        u1 (float): engine throttle [0-1]
        u2 (float): cvt ratio rate of change
        vehicle_resistive_force (float): resistive force of the vehicle due to drag and the like[N]
    
    Returns:
        float: engine speed rate of change [rps/s]
    """
    r = cvt_ratio*DRIVE_ASSEMBLY_RATIO
    
    vehicle_velocity = get_vehicle_velocity(cvt_ratio, engine_rps)
    vehicle_resistive_force = get_vehicle_resistive_force(vehicle_velocity)

    numerator = engine_torque - r*WHEEL_RADIUS*vehicle_resistive_force - r*DRIVE_ASSEMBLY_RATIO*u2*VEHICLE_INERTIA*engine_rps
    denominator = ENGINE_INERTIA + VEHICLE_INERTIA*r**2

    return numerator/denominator

def get_fuel_consumption(engine_torque, engine_rpm):
    """Compute the fuel consumption rate of the engine in grams/s
    
    Arguments:
        engine_torque (float): engine torque
        engine_rpm (float): engine speed
    """
    FUEL_CONSUMPTION_CONST = 0.001
    return FUEL_CONSUMPTION_CONST * engine_torque * engine_rpm


# test the functions
if __name__ == '__main__':
    # Test Torque interpolation function (check against torque map plotted in input_data)
    print(get_engine_torque(2000, 0.5))
    print(get_engine_torque(3000, 0.25))

    # Test vehicle rpm derivative function
    print(get_engine_rps_derivative(100, 2000, 0.5, 0.5))

