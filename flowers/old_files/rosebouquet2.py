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

def rotate_transform(X, Y, Z, angle):
    R = np.array([[np.cos(angle), -np.sin(angle), 0],
                  [np.sin(angle),  np.cos(angle), 0],
                  [0, 0, 1]])
    XYZ = np.stack([X.flatten(), Y.flatten(), Z.flatten()])
    XYZ_rotated = R @ XYZ
    X_rotated, Y_rotated, Z_rotated = XYZ_rotated.reshape(3, *X.shape)
    return X_rotated, Y_rotated, Z_rotated

def plot_3d_rose_bouquet():
    fig = go.Figure()
    colors = ['Reds', 'Purples', 'Greens', 'Blues', 'Greys', 'Hot']
    
    for i, color in enumerate(colors):
        X, Y, Z = meshgrid_transforms()
        angle = i * np.pi / 3
        X_rot, Y_rot, Z_rot = rotate_transform(X, Y, Z, angle)
        fig.add_trace(go.Surface(x=X_rot, y=Y_rot, z=Z_rot + i * 0.5, colorscale=color))
    
    fig.update_layout(title='3D Rose Bouquet Plot', autosize=True,
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))
    fig.show()

plot_3d_rose_bouquet()
