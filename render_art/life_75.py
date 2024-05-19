import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Define the grid size (52 weeks, 75 years)
rows, cols = 52, 75

# Create a figure and axis with 16:9 aspect ratio
fig, ax = plt.subplots(figsize=(16, 9))

# Generate a colormap
colors = plt.cm.rainbow(np.linspace(0, 1, rows * cols))

# Initialize the plot
scat = ax.scatter([], [], c=[], s=10)
# Make this font really pretty in WSL
count_text = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center', fontsize=15, fontname='DejaVu Sans')

# Set the limits and aspect ratio
ax.set_xlim(-1, cols)
ax.set_ylim(-1, rows)
ax.set_aspect('equal')

# Remove the axes
ax.axis('off')

# Track the color for each point
color_map = np.full((rows, cols), 'gray', dtype=object)

# Update function for animation
frames = rows * cols
updates_per_frame = 10  # Number of logical updates per rendered frame

def update_rendered_frame(rendered_frame):
    for _ in range(updates_per_frame):
        update_logic(rendered_frame * updates_per_frame + _)
    # Years is approximately what column we're on, out of 75. We want to show 1 decimal point though.
    years = round((rendered_frame * updates_per_frame) / cols, 1)
    label = 'Years: {}'.format(years)
    print(label)
    count_text.set_text(label)
    # if first frame, save a screenshot as png
    if rendered_frame == 0:
        plt.savefig('grid_of_dots.png')
    return scat, count_text

def update_logic(frame):
    j = frame // rows
    i = frame % rows
    if frame < rows * cols:
        color_map[i, j] = colors[frame]
    x = np.tile(np.arange(cols), rows)
    y = np.repeat(np.arange(rows), cols)
    colors_flat = color_map.flatten()
    scat.set_offsets(np.c_[x, y])
    scat.set_color(colors_flat)

# Create the animation
ani = animation.FuncAnimation(fig, update_rendered_frame, frames=frames // updates_per_frame, interval=1000 / 30, blit=True)

# Save the animation in 1080p
ani.save('./grid_of_dots_animation_1080p.mp4', writer='ffmpeg', dpi=80, fps=30, savefig_kwargs={'facecolor':'white'})

# Display the animation
# plt.show()

