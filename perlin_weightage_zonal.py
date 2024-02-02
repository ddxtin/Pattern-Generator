import matplotlib.pyplot as plt
from random import random

class Perlin:
    def __init__(self, scale=1.0):
        self.perm = [i for i in range(256)] * 2
        self.scale = scale

    def grad(self, hash, x):
        h = hash & 15
        grad = 1.0 + (h & 7)
        if h & 8:
            grad = -grad
        return grad * x

    def getValue(self, x):
        x0 = int(x * self.scale)
        x1 = x0 + 1

        t = x * self.scale - x0

        n0 = self.grad(self.perm[x0 & 255], t)
        n1 = self.grad(self.perm[x1 & 255], t - 1)

        return 0.395 * (n0 + n1)

def generate_pattern(params, perlin, two_color_prob):
    result_list = []
    count = params[0]["Count"]

    for i in range(count):
        x = i / count * 10
        value = perlin.getValue(x)
        result_list.append(value)

    # Normalize values between 0 and 1
    min_val = min(result_list)
    max_val = max(result_list)
    result_list = [(val - min_val) / (max_val - min_val) for val in result_list]

    # Apply two-color segments randomly
    for i in range(count):
        if random() < two_color_prob:  # Adjust the probability as needed
            result_list[i] = round(result_list[i])

    return result_list

def map_to_color(value):
    if value < 0.33:
        return 'A'
    elif 0.33 <= value < 0.66:
        return 'B'
    else:
        return 'C'

# # Input parameters
# input_params = [{"Count": 100}, {"A": 0.6, "B": 0.3, "C": 0.1}]
# colors = {'A': 'grey', 'B': 'black', 'C': 'blue'}

# # Perlin noise generator with increased scale (more noise)
# perlin = Perlin(scale=3.0)  # Adjust the scale factor as needed

# # Probability of having only two color segments in a region
# two_color_prob = 0.18  # Adjust the probability as needed

# # Generate and display a design
# pattern = generate_pattern(input_params, perlin, two_color_prob)

# fig, ax = plt.subplots(figsize=(10, 2))

# for i, value in enumerate(pattern):
#     category = map_to_color(value)
#     ax.bar(i, 1, color=colors[category])

# ax.set_xticks([])
# ax.set_yticks([])
# plt.show()
