import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from typing import List, Tuple

def meshgrid_transforms(x_offset: float = 0, y_offset: float = 0, z_offset: float = 0) -> tuple:
    """
    Calculate transformed meshgrid coordinates for 3D plotting.

    This function creates a meshgrid using trigonometric and exponential transformations
    to generate coordinates for a 3D visualization, specifically to plot a geometric
    structure with interesting undulations and rotations that mimic a rose. Offsets 
    can be applied to shift the entire structure along the x, y, and z axes.

    Args:
        x_offset (float): The offset to be added to all x-coordinates.
        y_offset (float): The offset to be added to all y-coordinates.
        z_offset (float): The offset to be added to all z-coordinates.

    Returns:
        tuple: A tuple of three numpy arrays (X, Y, Z), representing the x, y, and z
               coordinates after applying the transformations and offsets.
    """
    # Create meshgrid with transformations on the theta range
    xr, tr = np.meshgrid(np.linspace(0, 1, 25), np.linspace(0, 20 * np.pi, 1152) + 4 * np.pi)
 
    # Exponential decay function modulated by theta
    p = (np.pi / 2) * np.exp(-tr / (8 * np.pi))
    
    # Small amplitude sin wave used to introduce finer oscillations
    cr = np.sin(15 * tr) / 150
    
    # Modulation of amplitude with a decay and addition of fine oscillations
    u = 1 - (1 - np.mod(3.6 * tr, 2 * np.pi) / np.pi) ** 4 / 2 + cr
    
    # Radial coordinate transformation influenced by the exponential function
    yr = 2 * (xr**2 - xr)**2 * np.sin(p)
    
    # Calculating radial and height components based on the above transformations
    rr = u * (xr * np.sin(p) + yr * np.cos(p))
    hr = u * (xr * np.cos(p) - yr * np.sin(p))
    
    # Apply rotation and offset transformations to meshgrid
    return rr * np.cos(tr) + x_offset, rr * np.sin(tr) + y_offset, hr + z_offset + 0.35


def create_rose(fig: go.Figure, x_offset: float = 0, y_offset: float = 0, z_offset: float = 0, 
                angle_x: float = 0, angle_y: float = 0, angle_z: float = 0) -> None:
    """
    Add a 3D rose shape to a given Plotly figure using specified transformations.

    This function computes the meshgrid transformations to create the 3D coordinates for a rose,
    applies rotation transformations based on the provided angles, and adds the resulting surface
    to the given Plotly figure. The rose's position and orientation can be adjusted via offsets
    and rotation angles.

    Args:
        fig (go.Figure): The Plotly figure to which the rose will be added.
        x_offset (float): The offset to apply on the x-axis.
        y_offset (float): The offset to apply on the y-axis.
        z_offset (float): The offset to apply on the z-axis.
        angle_x (float): The rotation angle around the x-axis in radians.
        angle_y (float): The rotation angle around the y-axis in radians.
        angle_z (float): The rotation angle around the z-axis in radians.
    """
    # Generate the 3D coordinates for the rose shape with the given offsets
    X, Y, Z = meshgrid_transforms(x_offset, y_offset, z_offset)
    
    # Rotate the coordinates based on the specified angles
    X, Y, Z = rotate_xyz(X, Y, Z, angle_x, angle_y, angle_z)
    
    # Add the computed surface to the Plotly figure with a red color scale
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Reds', showscale=False))


def get_stem_top_center(height: float, x_offset: float, y_offset: float, curve_factor: float = 0.2,
                        angle_x: float = 0, angle_y: float = 0, angle_z: float = 0) -> tuple:
    """
    Calculate the top center position of a stem after applying a curve and rotation. The curvature 
    introduces a lateral displacement using sinusoidal functions that depend on the stem's height.

    Args:
        height (float): The height of the stem.
        x_offset (float): The offset to apply on the x-axis.
        y_offset (float): The offset to apply on the y-axis.
        curve_factor (float): The factor that determines the magnitude of the curvature.
        angle_x (float): The rotation angle around the x-axis in radians.
        angle_y (float): The rotation angle around the y-axis in radians.
        angle_z (float): The rotation angle around the z-axis in radians.

    Returns:
        tuple: A tuple containing the x, y, and z coordinates of the top center position after
               applying the curvature, offsets, and rotations.
    """
    # Calculate initial top center position with applied curve but no rotation
    z_top = height
    x_top = curve_factor * np.sin(np.pi * z_top / height) + x_offset
    y_top = curve_factor * np.cos(np.pi * z_top / height) + y_offset

    # Apply rotation transformations to the calculated position
    x_top, y_top, z_top = rotate_xyz(np.array([x_top]), np.array([y_top]), np.array([z_top]), angle_x, angle_y, angle_z)

    return x_top[0], y_top[0], z_top[0]


def rotate_xyz(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, angle_x: float = 0, 
               angle_y: float = 0, angle_z: float = 0) -> tuple:
    """
    Rotate a set of coordinates around the x, y, and z axes by given angles.

    This function applies a sequence of rotation transformations to 3D coordinates.
    Each rotation is performed around one of the principal axes (x, y, z), using the
    right-hand rule. The order of rotations is first around x, then y, and finally z.

    Args:
        X (np.ndarray): The x-coordinates of the points to rotate.
        Y (np.ndarray): The y-coordinates of the points to rotate.
        Z (np.ndarray): The z-coordinates of the points to rotate.
        angle_x (float): The rotation angle around the x-axis in radians.
        angle_y (float): The rotation angle around the y-axis in radians.
        angle_z (float): The rotation angle around the z-axis in radians.

    Returns:
        tuple: A tuple of numpy arrays (X, Y, Z), representing the coordinates after
               the rotations have been applied.
    """
    # Rotation around the x-axis
    Y_rot = Y * np.cos(angle_x) - Z * np.sin(angle_x)
    Z_rot = Y * np.sin(angle_x) + Z * np.cos(angle_x)
    Y, Z = Y_rot, Z_rot  # Update Y and Z after rotation around x-axis

    # Rotation around the y-axis
    X_rot = X * np.cos(angle_y) + Z * np.sin(angle_y)
    Z_rot = -X * np.sin(angle_y) + Z * np.cos(angle_y)
    X, Z = X_rot, Z_rot  # Update X and Z after rotation around y-axis

    # Rotation around the z-axis
    X_rot = X * np.cos(angle_z) - Y * np.sin(angle_z)
    Y_rot = X * np.sin(angle_z) + Y * np.cos(angle_z)
    X, Y = X_rot, Y_rot  # Update X and Y after rotation around z-axis

    return X, Y, Z


def create_stem(fig: go.Figure, height: float = 1, radius: float = 0.05, x_offset: float = 0, y_offset: float = 0, 
                z_offset: float = 0, curve_factor: float = 0.2, thorn_frequency: int = 5, angle_x: float = 0, 
                angle_y: float = 0, angle_z: float = 0) -> None:
    """
    Adds a 3D stem with optional thorns to a Plotly figure.

    This function creates a 3D cylindrical stem with curvature and thorns based on the provided parameters.
    It supports transformations such as rotation and translation (offsets), and allows customization of
    the stem's appearance through parameters such as height, radius, and curvature. The stem and thorns
    are then added to the provided Plotly figure object.

    Args:
        fig (go.Figure): The Plotly figure to which the stem will be added.
        height (float): The height of the stem.
        radius (float): The base radius of the stem.
        x_offset (float): Horizontal offset on the x-axis.
        y_offset (float): Horizontal offset on the y-axis.
        z_offset (float): Vertical offset along the z-axis.
        curve_factor (float): Factor that determines the magnitude of the stem's curvature.
        thorn_frequency (int): Frequency of thorns per unit height of the stem.
        angle_x (float): Rotation angle around the x-axis in radians.
        angle_y (float): Rotation angle around the y-axis in radians.
        angle_z (float): Rotation angle around the z-axis in radians.

    """
    # Create meshgrid for the stem geometry
    theta = np.linspace(0, 2 * np.pi, 30)
    z = np.linspace(0, height, 50)
    theta, z = np.meshgrid(theta, z)
    
    # Calculate the curvature components of the stem
    x_curve = curve_factor * np.sin(np.pi * z / height)
    y_curve = curve_factor * np.cos(np.pi * z / height)

    # Tapering effect for the stem's radius from base to top
    tapering = 1 - (z / height) * 0.3
    x = (radius * tapering * np.cos(theta)) + x_curve + x_offset
    y = (radius * tapering * np.sin(theta)) + y_curve + y_offset
    z = z + z_offset

    # Apply rotational transformations
    x, y, z = rotate_xyz(x, y, z, angle_x, angle_y, angle_z)

    # Add the stem's surface to the figure
    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Greens', showscale=False))
    
    # Generate thorns along the stem
    thorn_length = radius * 1.5
    num_thorns = int(height * thorn_frequency)
    for i in range(num_thorns):
        z_pos = (i / num_thorns) * height
        theta_pos = np.random.rand() * 2 * np.pi
        z_index = int(z_pos / height * 49)
        x_base = x_curve[z_index, 0] + x_offset
        y_base = y_curve[z_index, 0] + y_offset
        x_thorn = x_base + np.array([0, thorn_length * np.cos(theta_pos)])
        y_thorn = y_base + np.array([0, thorn_length * np.sin(theta_pos)])
        z_thorn = np.array([z_pos + z_offset, z_pos + z_offset - thorn_length / 4])
        
        # Apply rotational transformations to thorns
        x_thorn, y_thorn, z_thorn = rotate_xyz(x_thorn, y_thorn, z_thorn, angle_x, angle_y, angle_z)

        # Add thorns as lines to the figure
        fig.add_trace(go.Scatter3d(x=x_thorn, y=y_thorn, z=z_thorn, mode='lines', line=dict(color='Green', width=4)))


def plot_roses_and_stems(stem_specs: List[Tuple[float, float, float, float, float]]) -> None:
    """
    Plot a 3D visualization of roses and stems based on specified configurations.

    This function takes a list of specifications for multiple stems and roses,
    creates each one, and adds them to a Plotly figure. Each stem is topped with a rose,
    positioned based on the calculated top center of the stem. The function manages
    the addition of graphical components and the layout settings for the display.

    Args:
        stem_specs (list of tuple): A list of tuples, where each tuple contains parameters
            for a stem as (height, radius, x_offset, y_offset, z_offset).
    """
    
    fig = go.Figure()  # Initialize the Plotly figure

    # Iterate over each specification to plot the stems and corresponding roses
    for spec in stem_specs:
        height, radius, x_offset, y_offset, z_offset = spec
        # Create stem with a specified offset to account for the base height
        create_stem(fig, height, radius, x_offset, y_offset, z_offset + 1.5)
        
        # Calculate the top center position of the stem for placing the rose
        x_top, y_top, z_top = get_stem_top_center(height, x_offset, y_offset)
        
        # Place the rose at the calculated position with the correct z offset
        create_rose(fig, x_top, y_top, z_top + z_offset + 1.5)

    # Configure the layout of the figure to hide axis lines and adjust margins
    fig.update_layout(title='3D Roses and Stems Plot', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))
    fig.show()  # Display the figure

    
def create_asymmetrical_wrap(fig: go.Figure, base_radius: float = 0.05, top_radius: float = 0.8, height: float = 1.2, 
                             x_offset: float = 0, y_offset: float = 0, z_offset: float = 0, color: str = 'tan', 
                             angular_adjustments: np.ndarray = None) -> None:
    """
    Adds an asymmetrical wrap to a Plotly figure with customizable visual adjustments.

    This function generates an asymmetrical wrap shape based on specified parameters for
    radii, height, and angular adjustments. The wrap is modulated in both radial and z-directions
    to create an appealing visual effect. The generated shape is then added to a Plotly figure.

    Args:
        fig (go.Figure): The Plotly figure to which the wrap will be added.
        base_radius (float): The starting radius at the base of the wrap.
        top_radius (float): The nominal top radius of the wrap before adjustments.
        height (float): The height of the wrap from base to top.
        x_offset (float): Horizontal offset along the x-axis.
        y_offset (float): Horizontal offset along the y-axis.
        z_offset (float): Vertical offset along the z-axis.
        color (str): Color of the wrap.
        angular_adjustments (np.ndarray, optional): An array of values to adjust the radius at various angles.
            If None, no angular adjustments are applied.
    """
    # Define angles and vertical divisions for the wrap
    theta = np.linspace(0, 2 * np.pi, 60)
    z = np.linspace(0, height, 20)
    theta, z = np.meshgrid(theta, z)

    # Handle default case where no angular adjustments are specified
    if angular_adjustments is None:
        angular_adjustments = np.zeros_like(theta[0, :])  # Default to no adjustments

    # Calculate adjusted radii based on angular position
    top_radii = top_radius + 0.4 * np.sin(3 * theta[0, :] + angular_adjustments)

    # Interpolate between base and adjusted top radii
    r = np.linspace(base_radius, 1, z.shape[0])[:, None] * top_radii

    # Calculate coordinates in the xy-plane
    x = r * np.cos(theta) + x_offset
    y = r * np.sin(theta) + y_offset

    # Adjust z-values to add vertical extrusions for asymmetry
    z_extrusions = 0.5 * np.sin(2 * theta + angular_adjustments)  # Modulate z-values based on angle
    z = z + z_extrusions * (z / height)  # Increase modulation towards the top
    z += z_offset  # Apply vertical offset

    # Add the computed geometry to the figure as a surface plot
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.95, colorscale=[[0, color], [1, color]], showscale=False))


def plot_combined() -> str:
    """
    Creates a 3D visualization of a rose bouquet with an artistic wrap and returns the HTML representation.

    This function constructs a 3D visualization of a central rose surrounded by multiple tilted roses,
    set against an artistically wrapped background. The scene is built in a Plotly figure, which is then
    converted to HTML for easy embedding or display in web environments.

    Returns:
        str: An HTML string representing the 3D plot.
    """
    fig = go.Figure() # Initialize the Plotly figure

    # Create the central rose with a specific height and no slant
    create_stem(fig, height=3, radius=0.05, x_offset=0, y_offset=0, z_offset=0)
    x_top, y_top, z_top = get_stem_top_center(3, 0, 0)  # Calculate the top center for placing the rose
    create_rose(fig, x_top, y_top, z_top - 0.4)  # Add the rose to the figure

    # Configure and place additional roses in a circular arrangement
    num_around = 5
    radius = 1.0  # Horizontal distance for surrounding roses
    base_height = 2.8  # Height of the surrounding stems
    central_point = np.array([0, 0, 0])  # Reference central point at the base
    angles = np.linspace(0, 4 * np.pi, num_around, endpoint=False)  # Angles for positioning stems

    for i, angle in enumerate(angles):
        # Adjust slant angles for the stem
        distance = np.sqrt(radius**2 + base_height**2)  # Distance from base to rose top
        theta = np.arctan(radius / (base_height + 0.4))  # Reduce the effective height slightly for less slant
        angle_z = angle - np.pi / 2  # Adjust so that stems radiate outward

        # Create stems that originate from the same point but bend towards the top positions
        create_stem(fig, height=distance, radius=0.05, x_offset=central_point[0], y_offset=central_point[1], z_offset=central_point[2],
                    angle_x=theta, angle_y=0, angle_z=angle_z)

        # Calculate exact top center based on the rotation and position
        x_top, y_top, z_top = get_stem_top_center(distance, central_point[0], central_point[1], angle_x=theta, angle_y=0, angle_z=angle_z)

        # Attach roses at the calculated top positions
        create_rose(fig, x_offset=x_top, y_offset=y_top, z_offset=z_top-0.4)

    # Define angular adjustments for the wrap
    angular_adjustments = np.pi * np.cos(np.linspace(0, 2 * np.pi, 60))  # Modify this for desired asymmetry

    # Create an asymmetrical, artistic wrap around the bouquet
    create_asymmetrical_wrap(fig, base_radius=0.15, top_radius=2.15, height=2.3, x_offset=0, y_offset=0, z_offset=0.6, color='pink', angular_adjustments=angular_adjustments)

    # Update layout and show plot
    fig.update_layout(title={
                                'text': '3D Rose Bouquet with Artistic Bouquet Wrap',
                                "font": {
                                    "color": "#333333"
                                }, 
                            },
                      autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))

    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black'
    )

    fig.update_layout(
        scene=dict(
            camera=dict(
                eye=dict(x=-0.35, y=0.95, z=1.45),  # Changes where the camera is looking from
                up=dict(x=0, y=0, z=1),         # Sets the z-axis as up
                center=dict(x=0, y=0, z=0)      # Center of the scene
            )
        )
    ) 

    fig.update_layout(
        showlegend=False  
    )

    # Return HTML div as a string instead of showing the figure
    # fig.show()
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')


# ****
if __name__ == '__main__':
    # Plot the combined 3D rose bouquet with artistic wrap
    plot_html = plot_combined()

    # Save the plot to a file
    with open('rosebouquetplot.html', 'w') as f:
        f.write(plot_html)
