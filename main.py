import matplotlib.pyplot as plt
from random import choice

input_params = [{"Count": 130}, {"A": 0.4, "B": 0.3, "C": 0.2}]
colors = {'A': 'Black', 'B': 'Grey', 'C': "Purple"}

def generate_pattern(params):
    result_list = []
    count = params[0]["Count"]

    for key in params[1].keys():
        value = params[1][key]
        add_amount = int(value * count)

        for counter in range(add_amount):
            result_list.append(key)
    return result_list

populated_list = generate_pattern(input_params)
pattern = []

for i in range(input_params[0]["Count"]):
    pattern.append(choice(populated_list))

print(pattern)

# Plotting
fig, ax = plt.subplots(figsize=(10, 2))

for i, category in enumerate(pattern):
    ax.bar(i, 1, color=colors[category])

ax.set_xticks([])
ax.set_yticks([])

plt.show()


#######
# Original Code
# from random import choice
#
# input_params = [{"Count": 100}, {"A": 0.6, "B": 0.3, "C": 0.1}]
#
#
# def generate_pattern(params):
#     result_list = []
#     count = params[0]["Count"]
#
#     for key in params[1].keys():
#         value = params[1][key]
#         add_amount = int(value * count)
#
#         for counter in range(add_amount):
#             result_list.append(key)
#     return result_list
#
#
# populated_list = generate_pattern(input_params)
# pattern = []
#
# for i in range(input_params[0]["Count"]):
#     pattern.append(choice(populated_list))
#
# print(pattern)
########

