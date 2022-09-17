# 3d_printing_surface_generator
A repo with some code to mathematically define cylindrical surface shapes, which can be 3D-printed as vases, lamps and more.

## Getting started
The repo uses Python 3.9. To install Python dependencies, run:

```pip install -r requirements.txt```

Edit the run config and settings dictionary within `main.py` to modify the generated surface and how to output it. When finished, run:

```python main.py```

If the plot flag is set to true, a 3D plot of the surface will be shown in a web browser. 

If the save flag is set to true, the generated `.STL` file is located in the output folder specified, along with the settings and script used to generate the shape (this to ensure each saved shape can be recreated at a later time).
