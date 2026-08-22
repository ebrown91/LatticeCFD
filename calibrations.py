# Fusion strut daimeter to volume data

# for 5mm length BCC
BCCstrut_to_volume={
        0.5 : 6.183,
        1 : 22.296,
        1.5: 44.663,
        2: 69.611,
        2.5: 93.466
    }


#plot fusion derived data to check regression fit for interpolation
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

def plot_fusion_bcc_calibration(
    BCCstrut_to_volume,
    unit_cell_size,
    show_targets = None):
    '''
        Plot Fusion-derived BCC lattice calibration data.

    Parameters
    ----------
    BCCstrut_to_volume : dict
        Dictionary mapping strut diameter (mm) to measured
        solid volume (mm^3).

    unit_cell_size : float
        BCC unit-cell edge length in mm.

    show_targets : list, optional
        Porosity targets to highlight on the porosity plot.
        Example: [0.70, 0.75, 0.80, 0.85, 0.90]

    Returns
    -------
    dict
        Calculated calibration data.
   '''
    ##################### Strut diameter to volume solid regression #######################################
    data = sorted(BCCstrut_to_volume.items())
    strut_diameters = np.array([d for d,v in data])
    volume_solid = np.array([v for d, v in data]) 
    #starting with second order
    poly_model = Polynomial.fit(volume_solid, strut_diameters, deg =2)

    strut_diameter_pred = poly_model(volume_solid)

    residuals = strut_diameters-strut_diameter_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((strut_diameters-np.mean(strut_diameters))**2)
    r_squared = 1-(ss_res/ss_tot)
    
    coeffs = poly_model.convert().coef

    volume_solid_smooth = np.linspace(volume_solid.min(),volume_solid.max(), 100)
    strut_diameter_smooth = poly_model(volume_solid_smooth)
    
    volume_cell = unit_cell_size**3

    porosity = 1-(volume_solid/volume_cell)

    # Regression-predicted porosity
    porosity_smooth = 1 - (volume_solid_smooth / volume_cell)

    plt.figure(figsize=(7,5))

    plt.scatter(
        volume_solid,
        strut_diameters,
        marker ='o',
        label = "Actual Data"
    )

    plt.plot(volume_solid_smooth,strut_diameter_smooth, color= 'darkorange',
            linewidth = 2.5, label=f'2nd Order Fit($R^2 = {r_squared:.4f}$)')

    plt.xlabel("Strut Diameter (mm)")
    plt.ylabel("Solid Volume (mm^3)")
    plt.title("BCC Fusion Geometry: Solid Volume vs. Strut Diameter")
    plt.legend(fontsize = 11, loc = 'upper left')
    plt.grid(True, alpha = 0.3)
    plt.tight_layout()
    plt.show()
    
    ################################### strut diameter to porosity ##########################
    plt.figure(figsize=(7, 5))

    plt.scatter(
        strut_diameters,
        porosity * 100,
        marker="o"
    )

    plt.plot(strut_diameter_smooth, porosity_smooth*100, color= 'darkorange',
        linewidth = 2.5, label=f'2nd Order Fit($R^2 = {r_squared:.4f}$)')

    # Highlight target porosities
    if show_targets is not None:

        for target in show_targets:

            plt.axhline(
                target * 100,
                linestyle="--",
                alpha=0.5,
                label=f"{target:.0%}"
            )

        plt.legend(title="Target Porosity")

    plt.xlabel("Strut Diameter (mm)")
    plt.ylabel("Porosity (%)")
    plt.title(
        "BCC Fusion Geometry: "
        "Porosity vs. Strut Diameter"
    )

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Return calculated data
    # --------------------------------------------------------

    return {
        #"strut_diameter_mm": strut_diameters,
        #"solid_volume_mm3": volume_solid,
        #"porosity": porosity,
        "model": poly_model,
        
    }

calibration= plot_fusion_bcc_calibration(
    BCCstrut_to_volume,
    unit_cell_size = 5,
    show_targets = [0.70,0.75,0.80,0.85,0.90])