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

def generate_stem(height=1, radius=0.05, x_offset=0, y_offset=0, z_offset=0):
    theta = np.linspace(0, 2 * np.pi, 30)  # Angular coordinate
    z = np.linspace(0, height, 50)  # Linear coordinate along the height
    theta, z = np.meshgrid(theta, z)
    x = radius * np.cos(theta) + x_offset
    y = radius * np.sin(theta) + y_offset
    z = z + z_offset
    
    return x, y, z

def plot_roses_and_stems(rose_offsets, stem_specs):
    fig = go.Figure()

    # Plot each rose
    for offset in rose_offsets:
        x_offset, y_offset, z_offset = offset
        X, Y, Z = meshgrid_transforms(x_offset, y_offset, z_offset)
        fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Reds'))

    # Plot each stem
    for spec in stem_specs:
        height, radius, x_offset, y_offset, z_offset = spec
        X, Y, Z = generate_stem(height, radius, x_offset, y_offset, z_offset)
        fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Greens'))
    
    fig.update_layout(title='3D Roses and Stems Plot', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))
    fig.show()

# Example usage
rose_offsets = [
    (0, 0, -0.45),
    (1, 1, 0),
    (-1, -1, 0)
]

stem_specs = [
    (1, 0.05, 0, 0, -1),
    (1, 0.05, 1, 1, -1),
    (1, 0.05, -1, -1, -1)
]

plot_roses_and_stems(rose_offsets, stem_specs)
