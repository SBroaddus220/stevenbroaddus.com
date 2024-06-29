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

def plot_multiple_roses(offsets):
    fig = go.Figure()
    
    for offset in offsets:
        x_offset, y_offset, z_offset = offset
        X, Y, Z = meshgrid_transforms(x_offset, y_offset, z_offset)
        fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Reds'))
    
    fig.update_layout(title='3D Rose Plot', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))
    fig.show()

# Example usage
offsets = [
    (0, 0, 0),  # Original position
    (0, 0, 1),
    (1, 1, 0),  # Offset by 1 in the x and y directions
    (-1, -1, 0)  # Offset by -1 in the x and y directions
]

# Generates 50 roses in a grid pattern
for i in range(5):
    for j in range(10):
        offsets.append((i, j, 0))

plot_multiple_roses(offsets)
