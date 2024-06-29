import numpy as np
import plotly.graph_objects as go

def meshgrid_transforms(x_offset=0, y_offset=0, z_offset=0):
    xr, tr = np.meshgrid(np.linspace(0, 1, 25), np.linspace(0, 20 * np.pi, 1152) + 4 * np.pi)
    p = (np.pi / 2) * np.exp(-tr / (8 * np.pi))
    cr = np.sin(15 * tr) / 150
    u = 1 - (1 - np.mod(3.6 * tr, 2 * np.pi) / np.pi) ** 4 / 2 + cr
    yr = 2 * (xr**2 - xr)**2 * np.sin(p)
    rr = u * (xr * np.sin(p) + yr * np.cos(p))
    hr = u * (xr * np.cos(p) - yr * np.sin(p))
    return rr * np.cos(tr) + x_offset, rr * np.sin(tr) + y_offset, hr + z_offset + 0.35

def create_rose(fig, x_offset=0, y_offset=0, z_offset=0, angle_x=0, angle_y=0, angle_z=0):
    X, Y, Z = meshgrid_transforms(x_offset, y_offset, z_offset)
    X, Y, Z = rotate_xyz(X, Y, Z, angle_x, angle_y, angle_z)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Reds', showscale=False))


def get_stem_top_center(height, x_offset, y_offset, curve_factor=0.2, angle_x=0, angle_y=0, angle_z=0):
    # Initial top center calculation without rotation
    z_top = height
    x_top = curve_factor * np.sin(np.pi * z_top / height) + x_offset
    y_top = curve_factor * np.cos(np.pi * z_top / height) + y_offset
    z_top += 0  # No offset needed as z_top is already height

    # Apply rotation transformations
    x_top, y_top, z_top = rotate_xyz(np.array([x_top]), np.array([y_top]), np.array([z_top]), angle_x, angle_y, angle_z)

    return x_top[0], y_top[0], z_top[0]

def rotate_xyz(X, Y, Z, angle_x=0, angle_y=0, angle_z=0):
    # Rotation around the x-axis
    Y_rot = Y * np.cos(angle_x) - Z * np.sin(angle_x)
    Z_rot = Y * np.sin(angle_x) + Z * np.cos(angle_x)
    Y, Z = Y_rot, Z_rot

    # Rotation around the y-axis
    X_rot = X * np.cos(angle_y) + Z * np.sin(angle_y)
    Z_rot = -X * np.sin(angle_y) + Z * np.cos(angle_y)
    X, Z = X_rot, Z_rot

    # Rotation around the z-axis
    X_rot = X * np.cos(angle_z) - Y * np.sin(angle_z)
    Y_rot = X * np.sin(angle_z) + Y * np.cos(angle_z)
    X, Y = X_rot, Y_rot

    return X, Y, Z

def create_stem(fig, height=1, radius=0.05, x_offset=0, y_offset=0, z_offset=0, curve_factor=0.2, thorn_frequency=5, angle_x=0, angle_y=0, angle_z=0):
    theta = np.linspace(0, 2 * np.pi, 30)
    z = np.linspace(0, height, 50)
    theta, z = np.meshgrid(theta, z)
    x_curve = curve_factor * np.sin(np.pi * z / height)
    y_curve = curve_factor * np.cos(np.pi * z / height)
    tapering = 1 - (z / height) * 0.3
    x = (radius * tapering * np.cos(theta)) + x_curve + x_offset
    y = (radius * tapering * np.sin(theta)) + y_curve + y_offset
    z = z + z_offset

    x, y, z = rotate_xyz(x, y, z, angle_x, angle_y, angle_z)

    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Greens', showscale=False))
    
    # Adding thorns
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
        
        x_thorn, y_thorn, z_thorn = rotate_xyz(x_thorn, y_thorn, z_thorn, angle_x, angle_y, angle_z)

        fig.add_trace(go.Scatter3d(x=x_thorn, y=y_thorn, z=z_thorn, mode='lines', line=dict(color='Green', width=4)))

def plot_roses_and_stems(stem_specs):
    fig = go.Figure()

    # Plot each stem and corresponding rose at its top
    for spec in stem_specs:
        height, radius, x_offset, y_offset, z_offset = spec
        create_stem(fig, height, radius, x_offset, y_offset, z_offset + 1.5)
        # Calculate the top center of the stem
        x_top, y_top, z_top = get_stem_top_center(height, x_offset, y_offset)
        # Corrected addition for z_top with z_offset and additional height
        create_rose(fig, x_top, y_top, z_top + z_offset + 1.5)

    fig.update_layout(title='3D Roses and Stems Plot', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))
    fig.show()

    
def create_asymmetrical_wrap(fig, base_radius=0.05, top_radius=0.8, height=1.2, x_offset=0, y_offset=0, z_offset=0, color='tan', angular_adjustments=None):
    theta = np.linspace(0, 2 * np.pi, 60)
    z = np.linspace(0, height, 20)
    theta, z = np.meshgrid(theta, z)

    # Initialize top_radii to be uniformly the top_radius
    if angular_adjustments is None:
        angular_adjustments = np.zeros_like(theta[0, :])  # No adjustments by default

    # Apply angular adjustments which can vary the top radius at different angles
    top_radii = top_radius + 0.4 * np.sin(3 * theta[0, :] + angular_adjustments) 

    # Normalize the adjustments to vary smoothly across the wrap
    r = np.linspace(base_radius, 1, z.shape[0])[:, None] * top_radii

    x = r * np.cos(theta) + x_offset
    y = r * np.sin(theta) + y_offset

    # Adjust the z-values to create extrusions making the top part asymmetrical
    z_extrusions = 0.5 * np.sin(2 * theta + angular_adjustments)  # Modulate the z-values
    z = z + z_extrusions * (z / height)  # Apply the modulation more significantly towards the top
    z += z_offset  # Apply the base z offset

    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=.95, colorscale=[[0, color], [1, color]], showscale=False))


def plot_combined():
    fig = go.Figure()

    # Central rose with no slant
    create_stem(fig, height=3, radius=0.05, x_offset=0, y_offset=0, z_offset=0)
    x_top, y_top, z_top = get_stem_top_center(3, 0, 0)
    create_rose(fig, x_top, y_top, z_top - 0.4)

    # Parameters for surrounding roses
    num_around = 5
    radius = 1.0  # Horizontal distance from the center to the top of each surrounding rose
    base_height = 2.8  # Height of the surrounding stems
    central_point = np.array([0, 0, 0])  # Central point at the base
    angles = np.linspace(0, 4 * np.pi, num_around, endpoint=False)  # Generate angles for a pentagon

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

    # Additional independent rose heads on the floor
    # create_rose(fig, x_offset=-1.5, y_offset=-1.5, z_offset=0)  # First independent rose on the floor
    # create_rose(fig, x_offset=1.5, y_offset=-1.5, z_offset=0)  # Second independent rose on the floor

    # Define angular adjustments for the wrap
    angular_adjustments = np.pi * np.cos(np.linspace(0, 2 * np.pi, 60))  # Modify this for desired asymmetry

    # Create an asymmetrical, artistic wrap around the bouquet
    create_asymmetrical_wrap(fig, base_radius=0.15, top_radius=2.15, height=2.3, x_offset=0, y_offset=0, z_offset=0.6, color='pink', angular_adjustments=angular_adjustments)

    # Update layout and show plot
    fig.update_layout(title='3D Rose Bouquet with Artistic Bouquet Wrap', autosize=True,
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
        showlegend=False  # This will hide the legend
    )
    fig.show()

plot_combined()