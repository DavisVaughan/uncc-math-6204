from thomas import thomas_solver
from brennan import brennan_solver
from SOR import sor_solver
from PSOR import psor_solver

def get_solver_function(option_type, solver):

    if(option_type == "european"):
        if(solver == "direct"):
            solver_function = thomas_solver
        else:
            solver_function = sor_solver


    else: # American
        if(solver == "direct"):
            solver_function = brennan_solver
        else:
            solver_function = psor_solver

    return solver_function
