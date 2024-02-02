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

from flask import Flask, render_template, request, send_file, jsonify
from perlin_weightage_zonal import Perlin, generate_pattern, map_to_color
import matplotlib.pyplot as plt
from random import choice, random
from io import BytesIO
import json
from reportlab.pdfgen import canvas


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get input parameters from the form
    color1 = request.form['color1']
    weightage1 = float(request.form['weightage1'])
    color2 = request.form['color2']
    weightage2 = float(request.form['weightage2'])
    color3 = request.form['color3']
    weightage3 = float(request.form['weightage3'])
    perlin_scale = float(request.form['perlin_scale'])
    two_color_prob = float(request.form['two_color_prob'])

    # Input parameters
    input_params = [{"Count": 100}, {'A': weightage1, 'B': weightage2, 'C': weightage3}]
    colors = {'A': color1, 'B': color2, 'C': color3}

    # Perlin noise generator
    perlin = Perlin(scale=perlin_scale)

    # Generate and display a design
    pattern = generate_pattern(input_params, perlin, two_color_prob)

    fig, ax = plt.subplots(figsize=(10, 10))

    # text_output = []
    for i, value in enumerate(pattern):
        # text_output.append(colors[category])
        # category = map_to_color(value)
        ax.bar(i, 1, color=colors[pattern], align='edge', width=1, alpha=1, edgecolor='black', linewidth=0.5)
        # ax.text(i + 0.5, 0.5, category, ha='center', va='center', rotation=90, color='white', fontsize=10)

    ax.set_xticks([])
    ax.set_yticks([])

    # Save the generated image to a file
    file_path = 'static/design.png'
    plt.savefig(file_path)
    plt.close()

    return render_template('index.html', img_path=file_path, pattern=pattern)

@app.route('/download')
def download():
    # Serve the generated image for download
    return send_file('static/design.png', as_attachment=True)

@app.route('/download_pdf')
def download_pdf():
    pattern = json.loads(request.args.get('pattern'))

    # Create a PDF document with the pattern array
    pdf_data = BytesIO()
    c = canvas.Canvas(pdf_data)
    
    # Set up PDF content here, for example:
    c.drawString(100, 800, "Generated Pattern Array:")
    
    y_position = 780
    for index, color in enumerate(pattern):
        y_position -= 20
        c.drawString(100, y_position, f"{index + 1}. {color}")

    c.save()
    pdf_data.seek(0)

    return send_file(pdf_data, as_attachment=True, download_name='pattern.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
