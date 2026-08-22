from calibrations import calibration

import numpy as np
from scipy.interpolate import interp1d

def calc_strut(a,model,
              porosity_targets=None):
    
    d_struts = []
    for target in porosity_targets:
        volume_solid = (1-target)*a**3 #epsilon = 1- (volume_solid/volume_unit_cell)
        diameter_struts = model(volume_solid)
        d_struts.append(diameter_struts)


    d_struts = [round(float(d),3) for d in d_struts]
    #d_struts = [flaot(d) for d in d_struts] for FUSION
    return d_struts

#fitted model
diameter_model = calibration["model"]
print(calc_strut(5,diameter_model,
              porosity_targets=[0.7,0.75,0.8,0.85,0.9]))


