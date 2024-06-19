import matplotlib.pyplot as plt
import numpy as np

# Generate t values
t = np.linspace(0, 2 * np.pi, 1000)

# Create the plot
plt.figure(figsize=(8, 8))

# Plot 20 hearts with decreasing size
for i in range(20):
    scale = 1 - i * 0.05  # Decrease the size of each heart
    x = 16 * np.sin(t)**3 * scale
    y = (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) * scale
    plt.plot(x, y, color='red', linewidth=1)

# Set title and labels
plt.title('Te iubesc, Georgi')
plt.xlabel('Foarte mult')
plt.ylabel('Vorbesc serios')
plt.axhline(0, color='grey', linestyle='--', linewidth=0.5)
plt.axvline(0, color='grey', linestyle='--', linewidth=0.5)
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')

# Display the plot
plt.show()
