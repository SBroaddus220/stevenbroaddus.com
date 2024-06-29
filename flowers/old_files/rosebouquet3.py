import numpy as np
import plotly.graph_objects as go

def meshgrid_transforms():
    xr, tr = np.meshgrid(np.linspace(0, 1, 25), np.linspace(0, 20 * np.pi, 1152) + 4 * np.pi)
    p = (np.pi / 2) * np.exp(-tr / (8 * np.pi))
    cr = np.sin(15 * tr) / 150
    u = 1 - (1 - np.mod(3.6 * tr, 2 * np.pi) / np.pi) ** 4 / 2 + cr
    yr = 2 * (xr**2 - xr)**2 * np.sin(p)
    rr = u * (xr * np.sin(p) + yr * np.cos(p))
    hr = u * (xr * np.cos(p) - yr * np.sin(p))
    return rr * np.cos(tr), rr * np.sin(tr), hr + 0.35

def plot_3d_rose(offsets, colorscale='Reds'):
    fig = go.Figure()
    for offset in offsets:
        X, Y, Z = meshgrid_transforms()
        # Apply the offset to each component
        X += offset[0]
        Y += offset[1]
        Z += offset[2]
        fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=colorscale))
    
    # Ensure all axes have the same scale
    fig.update_layout(title='3D Rose Plot with Multiple Locations', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False),
                                 aspectmode='manual',
                                 aspectratio=dict(x=1, y=1, z=1)),  # Explicit aspect ratio
                      margin=dict(l=0, r=0, b=0, t=30))
    fig.show()

# Example usage: Placing roses at different coordinates
rose_offsets = [
    (0, 0, 0),   # Rose at origin
    (2, 2, 0),   # Rose shifted to the right and forward
    (-2, -2, 0), # Rose shifted to the left and backward
    (0, 4, 0)    # Rose further forward
]
plot_3d_rose(rose_offsets)
