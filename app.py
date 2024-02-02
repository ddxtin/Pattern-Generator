from flask import Flask, render_template, request, send_file, jsonify
from perlin_weightage_zonal import Perlin, generate_pattern, map_to_color
import matplotlib.pyplot as plt
from flaskwebgui import FlaskUI
from io import BytesIO
import json
from reportlab.pdfgen import canvas

app = Flask(__name__)

ui = FlaskUI(app=app, server="flask",  width=500, height=500) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get input parameters from the form
    strip_count = int(request.form['stripCount'])
    color1 = request.form['color1']
    weightage1 = float(request.form['weightage1'])
    color2 = request.form['color2']
    weightage2 = float(request.form['weightage2'])
    color3 = request.form['color3']
    weightage3 = float(request.form['weightage3'])
    color4 = request.form['color4']
    weightage4 = float(request.form['weightage4'])
    color5 = request.form['color5']
    weightage5 = float(request.form['weightage5'])
    perlin_scale = float(request.form['perlin_scale'])
    two_color_prob = float(request.form['two_color_prob'])

    # Input parameters
    input_params = [{"Count": strip_count}, {'A': weightage1, 'B': weightage2, 'C': weightage3, 'D': weightage4, 'E': weightage5}]
    global colors
    colors = {'A': color1, 'B': color2, 'C': color3, 'D': color4, 'E': color5}

    # Perlin noise generator
    perlin = Perlin(scale=perlin_scale)

    # Generate and display a design
    pattern = generate_pattern(input_params, perlin, two_color_prob)

    fig, ax = plt.subplots(figsize=(10, 10))

    for i, value in enumerate(pattern):
        category = map_to_color(value)
        ax.bar(i, 1, color=colors[category], align='edge', width=1, alpha=1, edgecolor='black', linewidth=0.5)
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

    # Create a PDF document with the pattern array and color names
    pdf_data = BytesIO()
    c = canvas.Canvas(pdf_data)
    
    # Set up PDF content here
    c.drawString(100, 800, "Generated Pattern Array with Color Names:")
    
    y_position = 780
    for index, (pattern_value, pattern_index) in enumerate(zip(pattern, range(1, len(pattern) + 1))):
        color_name = colors[map_to_color(pattern_value)]
        y_position -= 20

        if y_position < 50:
            c.showPage()  # Start a new page
            y_position = 780  # Reset y_position for the new page

        c.drawString(100, y_position, f"{index + 1}. {color_name}")

    c.save()
    pdf_data.seek(0)

    return send_file(pdf_data, as_attachment=True, download_name='pattern.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    ui.run()
