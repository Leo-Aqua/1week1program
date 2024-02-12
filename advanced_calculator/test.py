import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button

# Initial values
x_scale_init = 10
resolution_init = 100

# Generate initial x values and y values
x = np.linspace(-x_scale_init, x_scale_init, resolution_init)
y = x**2 + 3

# Plot the function
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
line, = plt.plot(x, y)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot of x^2 + 3')
plt.grid(True)

# Add textbox for x scale
ax_x_scale = plt.axes([0.25, 0.2, 0.65, 0.03])
text_box = TextBox(ax_x_scale, 'X scale', initial=str(x_scale_init))



def update_plot(event):
    x_scale = float(text_box.text)
    x = np.linspace(-x_scale, x_scale, resolution_init)
    y = x**2 + 3
    line.set_xdata(x)
    line.set_ydata(y)
    ax.set_xlim([-x_scale, x_scale])
    ax.set_ylim([0, x_scale**2 + 3])
    plt.draw()



text_box.on_submit(update_plot)

# Add coordinate system
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.show()