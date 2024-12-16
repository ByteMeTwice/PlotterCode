import matplotlib.pyplot as plt
import numpy as np

def create_spiral_circle(center_x, center_y, radius, line_width, fill_percentage):
    # Zeichne die Umrandung
    circle = plt.Circle((center_x, center_y), radius, color='black', fill=False, linewidth=line_width)
    plt.gca().add_artist(circle)

    # Maximale Anzahl der Umdrehungen basierend auf dem Radius und der Strichstärke berechnen
    max_turns = radius / (line_width / 2)
    turns = fill_percentage / 100 * max_turns

    # Erstellen der Spirale von innen nach außen
    t = np.linspace(0, turns * 2 * np.pi, int(1000 * turns))
    r = np.linspace(0, radius, len(t))
    x = center_x + r * np.cos(t)
    y = center_y + r * np.sin(t)

    # Zeichne die Spirale
    plt.plot(x, y, linewidth=line_width, color='black')

def create_calibration_circles(circle_diameter, min_line_width, max_line_width, line_width_step, output_path):
    # Berechnung der Strichstärken im angegebenen Intervall mit der Schrittweite
    line_widths = np.arange(min_line_width, max_line_width + line_width_step, line_width_step)

    # Anzahl der Kreise pro Zeile und Spalte
    num_circles = 11  # Anzahl der Kreise pro Zeile
    num_rows = len(line_widths)  # Anzahl der Zeilen

    # Größe der Figur in Millimetern berechnen
    width_mm = circle_diameter * num_circles
    height_mm = circle_diameter * num_rows

    # Erstelle die Figur mit exakten Abmessungen in mm
    fig = plt.figure(figsize=(width_mm / 25.4, height_mm / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width_mm)
    ax.set_ylim(0, height_mm)
    ax.axis('off')

    radius = circle_diameter / 2

    # Erstelle die Kreise
    for row, line_width in enumerate(line_widths):
        for col, fill_percentage in enumerate(np.linspace(100, 0, num_circles)):
            center_x = col * circle_diameter + radius
            center_y = row * circle_diameter + radius
            create_spiral_circle(center_x, center_y, radius, line_width, fill_percentage)

    # Speichere das Ergebnis als .svg mit den exakten Abmessungen
    plt.savefig(output_path, format='svg', bbox_inches='tight', pad_inches=0)
    plt.close()

# Parameter für die Kalibrierung
kreis_durchmesser = 2.5  # Durchmesser der Kreise in mm
min_strichstärke = 0.3  # Minimale Strichstärke in mm
max_strichstärke = 1  # Maximale Strichstärke in mm
strichstärke_schrittweite = 0.1  # Schrittweite der Strichstärke in mm
output_path = 'kalibrierung.svg'  # Pfad für die exportierte SVG-Datei

create_calibration_circles(kreis_durchmesser, min_strichstärke, max_strichstärke, strichstärke_schrittweite, output_path)
