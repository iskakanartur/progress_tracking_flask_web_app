############################## MULTI CIRCLE PLOT PROGRESS ###########################

import matplotlib.pyplot as plt
from math import pi
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
fig, ax = plt.subplots(figsize=(6, 6))
ax = plt.subplot(projection='polar')
data = [82, 12, 91]
startangle = 90
colors = ['#4393E5', '#43BAE5', '#7AE6EA']
xs = [(i * pi *2)/ 100 for i in data]
ys = [-0.2, 1, 2.2]
left = (startangle * pi *2)/ 360 #this is to control where the bar starts
# plot bars and points at the end to make them round
for i, x in enumerate(xs):
    ax.barh(ys[i], x, left=left, height=1, color=colors[i])
    ax.scatter(x+left, ys[i], s=350, color=colors[i], zorder=2)
    ax.scatter(left, ys[i], s=350, color=colors[i], zorder=2)
    
plt.ylim(-4, 4)
# legend
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Group A', markerfacecolor='#4393E5', markersize=10),
                  Line2D([0], [0], marker='o', color='w', label='Group B', markerfacecolor='#43BAE5', markersize=10),
                  Line2D([0], [0], marker='o', color='w', label='Group C', markerfacecolor='#7AE6EA', markersize=10)]
ax.legend(handles=legend_elements, loc='center', frameon=False)
# clear ticks, grids, spines
plt.xticks([])
plt.yticks([])
ax.spines.clear()
plt.show()
