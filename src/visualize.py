import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot_trajectory(df):
    """ Plotting the 3D Flight path """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    
    ax.plot(df["X"].values, df["Y"].values, df["Z"].values)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("3D Flight Path")
    ax.set_box_aspect([1, 1, 1])
    
    plt.tight_layout()
    plt.show()



def plot_attitude(df):
    """ Plot roll, pitch and yaw with respect to time   """

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    
    time = df["Time"].values
    roll = df["Roll (deg)"].values
    pitch = df["Pitch (deg)"].values
    yaw = df["Yaw (deg)"].values
    
    ax1.plot(time, roll)
    ax1.set_ylabel("Roll (deg)")

    ax2.plot(time, pitch)
    ax2.set_ylabel("Pitch (deg)")

    ax3.plot(time, yaw)
    ax3.set_ylabel("Yaw (deg)")
    ax3.set_xlabel("Time (s)")
    
    plt.tight_layout()
    plt.show()


def plot_map(df):
    """ Plot a 2D flight map that is altitude coloured  """

    fig, ax = plt.subplots(figsize=(8, 6))
    
    lon = df["Longitude"].values
    lat = df["Latitude"].values
    alt = df["Altitude"].values
    
    sc = ax.scatter(lon, lat, c=alt, s=2, cmap="viridis", rasterized=True) 
    plt.colorbar(sc, ax=ax, label="Altitude (m)")
    
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    ax.set_title("2D Flight Path (Altitude-Colored)")
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal", adjustable="box")
    
    plt.tight_layout()
    plt.show()


def plot_altitude(df):
    """ Plot altitude with respect to time   """

    plt.figure(figsize=(8, 4))
    
    plt.plot(df["Time"].values, df["Altitude"].values)
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.title("Altitude Over Time")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()


def animate_trajectory(df):
    """ Animate flight path replay in top-down view """

    fig, ax = plt.subplots(figsize=(8, 6))
    
    x_data = df["X"].values
    y_data = df["Y"].values
    
    ax.set_xlim(x_data.min(), x_data.max())
    ax.set_ylim(y_data.min(), y_data.max())
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title("Flight Replay (Top-Down)")
    
    point, = ax.plot([], [], "ro", markersize=8)
    path, = ax.plot([], [], "b-", linewidth=1, alpha=0.6)
    
    def update(i):
        point.set_data([x_data[i]], [y_data[i]])
        path.set_data(x_data[:i+1], y_data[:i+1])
        return point, path
    
    anim = FuncAnimation(fig, update, frames=len(df), interval=30, blit=True)
    plt.show()
    return anim