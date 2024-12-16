import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def create_spiral_circle(center_x, center_y, radius, line_width, fill_percentage):
    # Draw the outline
    circle = plt.Circle((center_x, center_y), radius, color='black', fill=False, linewidth=line_width)
    plt.gca().add_artist(circle)

    # Calculate max turns based on radius and line width
    max_turns = radius / (line_width / 2)
    turns = fill_percentage / 100 * max_turns

    # Create the spiral from inside out
    t = np.linspace(0, turns * 2 * np.pi, int(1000 * turns))
    r = np.linspace(0, radius, len(t))
    x = center_x + r * np.cos(t)
    y = center_y + r * np.sin(t)

    # Draw the spiral
    plt.plot(x, y, linewidth=line_width, color='black')


def create_filled_circles_from_image(width, height, circle_diameter, line_width, image_path, output_path,
                                     brightness_threshold=255):
    # Load and convert image to grayscale
    image = Image.open(image_path).convert('L')

    # Adjust brightness range
    image_array = np.array(image)
    min_val = np.min(image_array)
    max_val = np.max(image_array)
    image_array = ((image_array - min_val) / (max_val - min_val) * 255).astype(np.uint8)

    # Resize image to match sheet dimensions
    image = Image.fromarray(image_array)
    image = image.resize((int(width / circle_diameter), int(height / circle_diameter)), Image.LANCZOS)
    image_array = np.array(image)

    # Create figure
    fig = plt.figure(figsize=(width / 25.4, height / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    radius = circle_diameter / 2
    circle_count = 0  # Initialize counter

    # Draw circles based on image data and threshold
    for y in range(image_array.shape[0]):
        for x in range(image_array.shape[1]):
            brightness = image_array[y, x]
            if brightness < brightness_threshold:  # Only draw if below threshold
                center_x = x * circle_diameter + radius
                center_y = y * circle_diameter + radius
                fill_percentage = 100 - (brightness / 255 * 100)  # Inverse fill
                create_spiral_circle(center_x, center_y, radius, line_width, fill_percentage)
                circle_count += 1  # Increment counter

    # Save as SVG
    plt.savefig(output_path, format='svg', dpi=96)
    plt.close()

    return circle_count  # Return the count of circles


# Parameters
blatt_breite = 281.25  # Sheet width in mm
blatt_höhe = 373.5  # Sheet height in mm
kreis_durchmesser = 2.25  # Circle diameter in mm
strichstärke = 0.65  # Line width in mm
image_path = 'input_image.jpeg'  # Path to input image
output_path = 'output_image.svg'  # Path for SVG output
brightness_threshold = 256  # Adjust this value (0-255) for white exclusion

# Generate circles and get the count
circle_count = create_filled_circles_from_image(blatt_breite, blatt_höhe, kreis_durchmesser, strichstärke, image_path, output_path, brightness_threshold)

# Display the count
print(f"Number of circles: {circle_count}")
