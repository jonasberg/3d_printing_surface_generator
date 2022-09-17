import numpy as np

from generate_shape import generate_shape


# Run Config
# ===============
SHOW_PLOT = True
SAVE = False
OUTPUT_DIR = "output_surfaces"
MODEL_NAME = "Spiral Vase v.1"
# ===============

settings = {
    # Dimension and resolution of mesh
    "height_mm": 250,
    "n_circumferential_steps": 800,
    "n_vertical_steps": 100,

    # The pipeline of functions to apply to generate the surface.
    # For details on which functions are available, see surface_functions.py
    "functions_pipeline": [
        {
            "function_class": "Cylinder",
            "settings": {
                "base_radius_mm": 50
            }
        },
        {
            "function_class": "VerticalSineShape",
            "settings": {
                "magnitude": 0.8,
                "start_angle": np.pi / 4,
                "end_angle": 5 * np.pi / 6
            }
        },
        {
            "function_class": "VerticalSpiralPattern",
            "settings": {
                "n_vertical_turns": 0.1,
                "n_circumferential_periods": 2,
                "magnitude": 0.3,
                "absolute_sine": True,
                "vertical_turns_exponent": 1,
                "pattern_falloff_exponent": 0,
                "sine_twist_magnitude": 0.15
            }
        },
        {
            "function_class": "VerticalSpiralPattern",
            "settings": {
                "n_vertical_turns": 0.1,
                "n_circumferential_periods": 20,
                "magnitude": 0.025,
                "absolute_sine": False,
                "vertical_turns_exponent": 1,
                "pattern_falloff_exponent": 0,
                "sine_twist_magnitude": 0.1
            }
        }
    ]
}

if __name__ == "__main__":
    generate_shape(
        settings, 
        show_plot=SHOW_PLOT, 
        save=SAVE, 
        output_dir=OUTPUT_DIR, 
        output_dir_model_name=MODEL_NAME
    )