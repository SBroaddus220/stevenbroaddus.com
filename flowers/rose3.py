import numpy as np
import plotly.graph_objects as go

def draw_frame_plotly(f):
    f = (f - 2) % 48 + 1

    # Rose Part
    openness = 1.05 - np.cos(np.pi * f / (48 / 2.5)) * (1 - f / 48) ** 2
    opencenter = openness * 0.2
    pnum = 3.6
    nr = 30
    pr = 10
    B = 1.27689
    npetal = 40
    petalsep = 5 / 4

    petal_theta = (1 / pnum) * np.pi * 2
    nt = npetal * pr + 1

    r = np.linspace(0, 1, nr)
    theta = np.linspace(0, npetal * petal_theta, nt)
    R, THETA = np.meshgrid(r, theta)

    M = (1 - np.mod(pnum * THETA, 2 * np.pi) / np.pi)
    x = 1 - (petalsep * M**2 - 1/4)**2 / 2

    phi = (np.pi / 2) * np.linspace(opencenter, openness, nt)**2
    phi = phi[:, np.newaxis]  # Reshape phi to match dimensions with R
    y = 1.995 * (R**2) * (B * R - 1)**2 * np.sin(phi)
    R2 = x * (R * np.sin(phi) + y * np.cos(phi))
    X = R2 * np.sin(THETA)
    Y = R2 * np.cos(THETA)
    Z = x * (R * np.cos(phi) - y * np.sin(phi)) * 1

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Reds')])
    fig.update_layout(title='3D Rose Animation Frame', autosize=True,
                      scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)),
                      margin=dict(l=0, r=0, b=0, t=30))
    fig.show()

draw_frame_plotly(24)  # Test drawing frame
