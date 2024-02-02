from random import choice

input_params = [{"Count": 100}, {"A": 0.6, "B": 0.3, "C": 0.1}]

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
