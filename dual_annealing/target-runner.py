#!/usr/bin/env python3
###############################################################################
# This script is the command that is executed every run.
# Check the examples in examples/
#
# This script is run in the execution directory (execDir, --exec-dir).
#
# PARAMETERS:
# argv[1] is the candidate configuration number
# argv[2] is the instance ID
# argv[3] is the seed
# argv[4] is the instance name
# The rest (argv[5:]) are parameters to the run
#
# RETURN VALUE:
# This script should print one numerical value: the cost that must be minimized.
# Exit with 0 if no error, with 1 in case of error
###############################################################################

import sys
import numpy as np
from scipy.optimize import dual_annealing
import warnings


def from_01(x, xmin, xmax):
    return x * (xmax - xmin) + xmin

def rosenbrock(x):
    xmin = -1
    xmax = 1
    x = np.asarray(x)
    x = from_01(x, xmin = xmin, xmax = xmax)
    r = np.sum(100.0 * (x[1:] - x[:-1]**2.0)**2.0 + (1 - x[:-1])**2.0,
               axis=0)
    return r

def rastrigin(x):
    xmin = -5.12
    xmax = 5.12
    x = np.asarray(x)
    x = from_01(x, xmin = -1, xmax = 1)
    r = np.sum(x*x - 10*np.cos(2*np.pi*x)) + 10*np.size(x)
    return r


def stybtang(x):
    xmin = -5
    xmax = 5
    x = np.asarray(x)
    x = from_01(x, xmin = xmin, xmax = xmax)
    r = np.sum(x**4 - 16*x**2 + 5*x)
    return r

def michalewicz(x):
    xmin = 0
    xmax = np.pi
    x = np.asarray(x)
    x = from_01(x, xmin = xmin, xmax = xmax)
    d = np.size(x)
    i = np.arange(1, d + 1)
    m = 10
    r = np.sum(np.sin(x) * np.sin(i * x * x / np.pi)**(2 * m))
    return r
    
def ackley(x):
    shift = [-0.4] + [1.25] * (np.size(x) - 1)
    xmin = -32
    xmax = 32
    x = np.asarray(x)
    x = from_01(x, xmin = xmin, xmax = xmax)
    x = x + shift
    a = 20
    b = 0.2
    c = 2 * np.pi
    r = -a * np.exp(-b * np.sqrt(np.sum(x**2)/np.size(x))) \
        - np.exp(np.sum(np.cos(c * x))/np.size(x)) + a + np.exp(1)
    return r

instance2fun = {
    "ackley" : ackley,
    "michalewicz" : michalewicz,
    "stybtang" : stybtang,
    "rastrigin": rastrigin,
    "rosenbrock" : rosenbrock,
}

if __name__=='__main__':
    if len(sys.argv) < 5:
        print("\nUsage: ./target-runner.py <configuration_id> <instance_id> <seed> <instance_name> <dim> <list of parameters>\n")
        sys.exit(1)

    # Get the parameters as command line arguments.
    configuration_id = sys.argv[1]
    instance_id = sys.argv[2]
    seed = int(sys.argv[3])
    instance = sys.argv[4]
    dim = int(sys.argv[5].split("=")[1])
    cand_params = sys.argv[6:]

    # Parse parameters
    args = {}
    while cand_params:
        # Get and remove first and second elements.
        param = cand_params.pop(0)
        if not param.startswith("--"):
            target_runner_error(f"unknown parameter {param}")
        param = param[2:] # Remove --
        param, value = param.split('=')
        
        if param in ["initial_temp", "restart_temp_ratio", "visit", "accept"]:
            value = float(value)
        elif param == "no_local_search":
            value = value == "1"
        else:
            target_runner_error(f"unknown parameter {param}")            

        args[param] = value
    
    lw = [0.0] * dim
    up = [1.0] * dim
    # Gives warnings for some configurations so ignore them.
    # We could reject those configurations by returning Inf.
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    ret = dual_annealing(instance2fun[instance],
                         bounds=list(zip(lw, up)), maxiter=500, maxfun = 1e4,
                         seed = seed, **args)
    print(f'{ret.fun}\n')
    sys.exit(0)

# Useful function to print errors.
def target_runner_error(msg):
    print("target-runner.py: error: " + msg)
    sys.exit(1)

    
