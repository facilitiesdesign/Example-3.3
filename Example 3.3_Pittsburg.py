# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    # Create lists
    plant = ['Albany', 'Little Rock', 'Pittsburg']
    warehouse = ['Boston', 'Philadephia', 'Galveston', 'Raleigh']
    supply = [250, 300, 880]
    demand = [200, 100, 300, 280]
    cost = [ 
            [10, 15, 22, 20], #Albany plant
            [19, 15, 10, 9], #Little Rock plant
            [17, 8, 18, 12] #Pittsburg plant
            ]
    # Indices
    P = len(plant)
    W = len(warehouse)
    
    # Make dictionaries
    supply_dict = {plant[i]: supply[i] for i in range(P)}
    demand_dict = {warehouse[j] : demand[j] for j in range(W)}
    cost_dict = {(plant[i], warehouse[j]) : cost[i][j] for i in range(P) for j in range(W)}
    
    # Write model
    m = Model("Example 3.3")
    
    # Decision variable
    x = m.addVars(range(P), range(W), lb = 0, vtype = GRB.CONTINUOUS, name = "Volume")
    
    # Objective fuction
    m.setObjective(quicksum(cost[i][j] * x[i,j] for i in range(P) for j in range(W)), GRB.MINIMIZE)
    
    # Write Constraints
    for i in range(P):
        m.addConstr(quicksum(x[i,j] for j in range(W)) <= supply[i], name = "Supply_Constraint")
                    
    for j in range(W):
        m.addConstr(quicksum(x[i,j] for i in range(P)) >= demand[j], name = "Demand_Constraint")

    # Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
       for v in m.getVars():
           if v.x > 0:
               print('%s = %g' % (v.varName, v.x)) 
       print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
       print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
       print('LP is unbounded.')
except GurobiError:
    print('Error reported')