import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def draw_frame(f):
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

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    C = np.sqrt(X**2 + Y**2 + Z**2 * 0.9)
    ax.plot_surface(X, Y, Z, facecolors=cm.jet(C / C.max()), edgecolor='none')

    ax.set_aspect('auto')
    ax.axis('off')
    plt.show()

draw_frame(24)  # Test drawing frame
