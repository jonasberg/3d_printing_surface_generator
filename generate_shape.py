import os
import json
from shutil import copyfile
from datetime import datetime

import numpy as np
from stl import mesh
from scipy.spatial import Delaunay
import plotly.figure_factory as ff

from surface_functions import *


def generate_shape(settings, show_plot=True, save=False, 
                    output_dir="output_surfaces", output_dir_model_name="model"):
    # Set up cylindic coordinate system; radius is determined by surface functions
    phi = np.linspace(0, 2*np.pi, settings["n_circumferential_steps"])
    h = np.linspace(0, 1, settings["n_vertical_steps"])

    # Join functions into chain
    f_total = None
    for f_dict in settings["functions_pipeline"]:
        # Fetch the class specified in f_dict
        c_name = f_dict["function_class"]
        c = surface_functions_catalog[c_name]
        
        # Initialize the function with the specified settings
        f_settings = f_dict["settings"]
        f = c(f_settings)
        
        # Add the function to the pipeline
        f_total = f.apply(f_total)

    # Turn cylindric coordinate axes into mesh
    phi, h = np.meshgrid(phi, h)
    phi = phi.flatten()
    h = h.flatten()

    # Apply chain in coordinate transform to euclidian space
    x = f_total(phi, h) * np.cos(phi)
    y = f_total(phi, h) * np.sin(phi)
    z = settings["height_mm"] * h

    # Join points into simplices; same simplices are used in euclidian space
    points2D = np.vstack([phi,h]).T
    tri = Delaunay(points2D)
    simplices = tri.simplices

    if show_plot:
        fig = ff.create_trisurf(x=x, y=y, z=z,
            simplices=simplices,
            title="Torus", 
            aspectratio=dict(x=1, y=1, z=1), 
            colormap=['#FFFFFF','#FFFFFF']
        )

        fig.show()
    
    if save:
        # Generate mesh to save as STL
        data = np.zeros(len(simplices), dtype=mesh.Mesh.dtype)

        # Iterate over each simplex
        for i, sim in enumerate(simplices):
            x1, x2, x3 = x[sim]
            y1, y2, y3 = y[sim]
            z1, z2, z3 = z[sim]
            
            p1 = [x1, y1, z1]
            p2 = [x2, y2, z2]
            p3 = [x3, y3, z3]
            
            data["vectors"][i] = np.array([p1, p2, p3])
            
        m=mesh.Mesh(data)

        # Create output dir
        output_dir = os.path.join(
            ".", 
            output_dir, 
            output_dir_model_name,
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        )
        os.makedirs(output_dir, exist_ok=True)

        # Save mesh
        m.save(os.path.join(output_dir, 'surface.stl'))

        # Save copy of settings used
        with open(os.path.join(output_dir, "settings.json"), "w") as f:
            json.dump(settings, f, indent=4)
            
        # Save copy of functions and routine to generate plot used
        copyfile(
            os.path.join(".", "surface_functions.py"),
            os.path.join(output_dir, "surface_functions.py")
        )

        copyfile(
            os.path.join(".", "generate_shape.py"),
            os.path.join(output_dir, "generate_shape.py")
        )