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

def create_rose(fig, x_offset=0, y_offset=0, z_offset=0):
    X, Y, Z = meshgrid_transforms(x_offset, y_offset, z_offset)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Reds', showscale=False))

def get_stem_top_center(height, x_offset, y_offset, curve_factor=0.2):
    z_top = height
    x_top = curve_factor * np.sin(np.pi * z_top / height) + x_offset
    y_top = curve_factor * np.cos(np.pi * z_top / height) + y_offset
    return x_top, y_top, z_top


def create_stem(fig, height=1, radius=0.05, x_offset=0, y_offset=0, z_offset=0, curve_factor=0.2, thorn_frequency=5):
    theta = np.linspace(0, 2 * np.pi, 30)
    z = np.linspace(0, height, 50)
    theta, z = np.meshgrid(theta, z)
    x_curve = curve_factor * np.sin(np.pi * z / height)
    y_curve = curve_factor * np.cos(np.pi * z / height)
    tapering = 1 - (z / height) * 0.3
    x = (radius * tapering * np.cos(theta)) + x_curve + x_offset
    y = (radius * tapering * np.sin(theta)) + y_curve + y_offset
    z = z + z_offset
    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Greens', showscale=False))
    
    # Adding thorns
    thorn_length = radius * 1.5
    num_thorns = int(height * thorn_frequency)
    for i in range(num_thorns):
        z_pos = (i / num_thorns) * height
        theta_pos = np.random.rand() * 2 * np.pi
        z_index = int(z_pos / height * 49)  # Compute the closest z index, 49 is max index in z
        x_base = x_curve[z_index, 0] + x_offset
        y_base = y_curve[z_index, 0] + y_offset
        x_thorn = [x_base, x_base + thorn_length * np.cos(theta_pos)]
        y_thorn = [y_base, y_base + thorn_length * np.sin(theta_pos)]
        z_thorn = [z_pos + z_offset, z_pos + z_offset - thorn_length / 4]  # Extend thorn slightly downwards
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


def plot_combined():
    fig = go.Figure()

    # Plot multiple roses with stems
    stem_specs = [
        (3.5, 0.05, -2, 0, -1),  # Adjusted x_offset to align all elements
        (3, 0.05, -1.5, 1, -1),
        (2.8, 0.05, -2.5, -1, -1)
    ]
    for spec in stem_specs:
        height, radius, x_offset, y_offset, z_offset = spec
        create_stem(fig, height, radius, x_offset, y_offset, z_offset + 1.5)
        x_top, y_top, z_top = get_stem_top_center(height, x_offset, y_offset)
        create_rose(fig, x_top, y_top, z_top + z_offset + 1.1)

    # Adding an independent stem
    create_stem(fig, height=2, radius=0.05, x_offset=1, y_offset=1, z_offset=0)

    # Adding an independent rose
    create_rose(fig, x_offset=2, y_offset=1, z_offset=0)

    fig.update_layout(title='Combined 3D Roses and Stems Plot', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))
    fig.show()

plot_combined()
