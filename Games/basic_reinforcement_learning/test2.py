import numpy as np
import matplotlib.pyplot as plt
import pdb

# Define the payoff matrix
A = np.array([[3, 0],
              [5, 1]])

B = np.array([[3, 5],
              [0, 1]])

# Define the range of x and y values to plot
x = np.arange(0, 1.1, 0.1)
y = np.arange(0, 1.1, 0.1)

# Create a meshgrid from the x and y values
X, Y = np.meshgrid(x, y)

# Define the differential equations for the probabilities of the actions
dX = X*(A[0,0] - A[1,0]*Y) + (A[0,1] - A[1,1]*Y)
dY = Y*(A[1,1] - A[0,1]*X) + (A[1,0] - A[0,0]*X)

# Normalize the differential equations
norm = np.sqrt(dX**2 + dY**2)
dX /= norm
dY /= norm

pdb.set_trace()
print(dX.shape)

# Plot the directional field using quiver
plt.quiver(X, Y, dX, dY)

# Add labels and title to the plot
plt.xlabel('Probability of Player 1 playing Action 1')
plt.ylabel('Probability of Player 2 playing Action 1')
plt.title('Directional Field of Probabilities in Matrix Game')

# Show the plot
plt.show()
