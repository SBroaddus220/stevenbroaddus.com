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


def plot_rose_head() -> str:
    """
    Creates and returns the HTML representation of a 3D visualization focused solely on a rose head.
    
    The function initializes a Plotly figure and adds a single rose head at the origin. The layout
    of the figure is configured to focus the viewer's attention directly on the rose head by hiding
    the axes and adjusting the camera's position. The background and plot colors are set to black
    to highlight the rose head, and the legend is hidden to maintain focus on the visual element.

    Returns:
        str: A string containing the HTML necessary to render the plot. The HTML includes the CDN
             link to the required Plotly JavaScript, allowing the plot to be embedded directly in
             web pages without needing additional files.
    """
    fig = go.Figure()  # Initialize the Plotly figure

    # Add only a rose head at the origin
    create_rose(fig, x_offset=0, y_offset=0, z_offset=0)  # Add the rose to the figure

    # Configure the layout of the figure to hide axis lines and adjust margins
    fig.update_layout(title='3D Rose Head', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))

    fig.update_layout(
        scene=dict(
            camera=dict(
                eye=dict(x=1.75, y=-2, z=2),  # Adjust camera to focus on the rose head
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
    # Plot a single 3D rose head and save the HTML to a file 
    plot_html = plot_rose_head()
    with open('rose-head-plot.html', 'w') as f:
        f.write(plot_html)