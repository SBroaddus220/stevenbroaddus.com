import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

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


def plot_single_rose() -> str:
    """
    Generates an HTML string for a 3D visualization of a single rose with its stem.
    
    This function creates a Plotly figure to model a single rose complete with its stem.
    The stem is modeled first, followed by the rose positioned at the calculated top center of the stem.
    The layout is specifically tailored to enhance the 3D effect and focus on the rose. The camera,
    background color, and visibility settings are adjusted to optimize the viewer's experience.
    The generated HTML includes the necessary Plotly JavaScript from CDN, enabling direct embedding into web pages.
    
    Returns:
        str: HTML string for embedding the 3D plot, which includes CDN links to Plotly's JavaScript resources.
    """
    fig = go.Figure()  # Initialize the Plotly figure

    # Create a single stem and rose
    create_stem(fig, height=3, radius=0.05, x_offset=0, y_offset=0, z_offset=0)
    x_top, y_top, z_top = get_stem_top_center(3, 0, 0)  # Calculate the top center for placing the rose
    create_rose(fig, x_top, y_top, z_top - 0.4)  # Add the rose to the figure

    # Configure the layout of the figure to hide axis lines and adjust margins
    fig.update_layout(title='3D Rose', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))

    fig.update_layout(
        scene=dict(
            camera=dict(
                eye=dict(x=-1.75, y=1.75, z=1.75),  # Changes where the camera is looking from
                up=dict(x=0, y=0, z=1),         # Sets the z-axis as up
                center=dict(x=0, y=0, z=0)      # Center of the scene
            )
        )
    )

    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black'
    )

    fig.update_layout(
        showlegend=False  
    )

    # Convert figure to HTML
    plot_html = pio.to_html(fig, full_html=True, include_plotlyjs='cdn')
    
    return plot_html


# ****
if __name__ == '__main__':
    # Plot a single 3D rose and save the HTML to a file 
    plot_html = plot_single_rose()
    with open('rose-plot.html', 'w') as f:
        f.write(plot_html)
