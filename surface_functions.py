import numpy as np
import plotly.figure_factory as ff
from scipy.spatial import Delaunay


class Cylinder():
    """
    Base Class for all cylindric geometries - should start each chain.
    """
    def __init__(self, settings):
        self.settings = settings
        self.base_radius_mm = settings["base_radius_mm"]


    def apply(self, _):
        return lambda phi, h: self.base_radius_mm

class VerticalSineShape():
    """
    Multiplies the radius with a fraction of a vertical sine wave (with offset).

    Useful to create vase like structures, which can be wider at the base and
    thinner at the top.
    """
    def __init__(self, settings):
        self.settings = settings
        self.magnitude = settings["magnitude"]
        self.start_angle = settings["start_angle"]
        self.end_angle = settings["end_angle"]

    def _wave(self):
        return lambda x: np.sin(x + self.start_angle)

    def _shape_func(self, phi, h):
        wave = self._wave()
        return self.magnitude * (wave(h * self.end_angle))

    def apply(self, f_prev):
        return lambda phi, h: f_prev(phi, h) * (1 + self._shape_func(phi, h))

class VerticalSpiralPattern():
    """
    Adds a vertical spiral pattern to the surface.

    Uses a base circumferential sine shape, which is rotated as the 
    z-coordinate increases. Additional parameters can tweak how the spiral
    is shaped. 
    """
    def __init__(self, settings):
        self.settings = settings
        self.n_vertical_turns = settings["n_vertical_turns"]
        self.n_circumferential_periods = settings["n_circumferential_periods"]
        self.magnitude = settings["magnitude"]
        self.absolute_sine = settings["absolute_sine"]
        self.vertical_turns_exponent = settings["vertical_turns_exponent"]
        self.pattern_falloff_exponent = settings["pattern_falloff_exponent"]
        self.sine_twist_magnitude = settings["sine_twist_magnitude"]
        

    def _circumferential_length(self):
        # Bad naming, but it is the angle needed to rotate the circumferential pattern one full revolution
        return self.n_circumferential_periods * 2 * np.pi

    def _wave(self):
        if self.absolute_sine:
            return lambda x: np.abs(np.sin(x))
        else:
            return np.sin

    def _spiral_func(self):
        wave = self._wave()
        return lambda phi, h: (
            self.magnitude * 
            wave(
                self.n_circumferential_periods * phi + 
                self._circumferential_length() * self.n_vertical_turns * h**self.vertical_turns_exponent -
                self._circumferential_length() * self.sine_twist_magnitude * np.cos(h * np.pi) **self.vertical_turns_exponent 
            )
        )

    def _falloff_function(self):
        spiral_func = self._spiral_func()
        return lambda phi, h: spiral_func(phi, h) * np.sin(np.pi*h)**self.pattern_falloff_exponent

    def apply(self, f_prev):
        total_spiral_func = self._falloff_function()
        return lambda phi, h: f_prev(phi, h) * (1 + total_spiral_func(phi, h))

class RadialSinePattern():
    """
    Adds a circumferential sine wave pattern.
    """
    def __init__(self, settings):
        self.settings = settings
        self.magnitude = settings["magnitude"]
        self.n_circumferential_periods = settings["n_circumferential_periods"]
        self.pattern_falloff_exponent = settings["pattern_falloff_exponent"]

    def _wave(self):
        return np.sin

    def _radial_sine_func(self):
        wave = self._wave()
        return lambda phi, h: self.magnitude*wave(self.n_circumferential_periods * phi)

    def _falloff_function(self):
        radial_sine_func = self._radial_sine_func()
        return lambda phi, h: radial_sine_func(phi, h) * np.sin(np.pi*h)**self.pattern_falloff_exponent
        
    def apply(self, f_prev):
        total_radial_sine_func = self._falloff_function()
        return lambda phi, h: f_prev(phi, h) * (1 + total_radial_sine_func(phi, h))

class RadialZigZagPattern():
    """
    Adds a circumferential zig-zag pattern.
    """
    def __init__(self, settings):
        self.settings = settings
        self.magnitude = settings["magnitude"]
        self.n_circumferential_periods = settings["n_circumferential_periods"]
        self.pattern_falloff_exponent = settings["pattern_falloff_exponent"]

    def _wave(self):
        def zig_zag(x):
            x = x % (2 * np.pi)
            x *= 2 / np.pi

            ind = (x > 1) * (x <= 3)
            x[ind] = 2 - x[ind]

            ind = x > 3
            x[ind] = x[ind] - 4

            return x

        return zig_zag

    def _radial_zig_zag_func(self):
        wave = self._wave()
        return lambda phi, h: self.magnitude*wave(self.n_circumferential_periods * phi)

    def _falloff_function(self):
        radial_zig_zag_func = self._radial_zig_zag_func()
        return lambda phi, h: radial_zig_zag_func(phi, h) * np.sin(np.pi*h)**self.pattern_falloff_exponent
        
    def apply(self, f_prev):
        total_radial_zig_zag_func = self._falloff_function()
        return lambda phi, h: f_prev(phi, h) * (1 + total_radial_zig_zag_func(phi, h))

surface_functions_catalog = {
    "Cylinder": Cylinder,
    "VerticalSineShape": VerticalSineShape,
    "VerticalSpiralPattern": VerticalSpiralPattern,
    "RadialSinePattern": RadialSinePattern,
    "RadialZigZagPattern": RadialZigZagPattern,
}