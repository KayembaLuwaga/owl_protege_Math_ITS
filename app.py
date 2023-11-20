from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_volume(shape, radius, side_length, base_length, height):
    if shape == "Sphere":
        volume_formula = f"V = \\frac{{4}}{{3}} \\pi r^3"
        volume_formula_with_values = f"V = \\frac{{4}}{{3}} \\pi {radius}^3"
        volume = (4/3) * 3.14 * radius**3
    elif shape == "Cube":
        volume_formula = f"V = s^3"
        volume_formula_with_values = f"V = {side_length}^3"
        volume = side_length**3
    elif shape == "Pyramid":
        volume_formula = f"V = \\frac{{1}}{{3}} \\times base^2 \\times height"
        volume_formula_with_values = f"V = \\frac{{1}}{{3}} \\times {base_length}^2 \\times {height}"
        volume = (1/3) * base_length**2 * height
    else:
        volume_formula = ""
        volume_formula_with_values = ""
        volume = None

    return volume_formula, volume_formula_with_values, volume

def get_label_and_value_for_shape(shape, radius, side_length, base_length, height):
    label = ""
    value = None

    if shape == "Sphere":
        label = "Radius"
        value = radius
    elif shape == "Cube":
        label = "Side Length"
        value = side_length
    elif shape == "Pyramid":
        label = "Base Length, Height"
        value = f"{base_length}, {height}"

    return label, value

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        shape = request.form['shape']

        # Initialize variables with default values
        radius = side_length = base_length = height = 0.0

        # Check if the form fields are not empty before converting to float
        if 'radius' in request.form and request.form['radius']:
            radius = float(request.form['radius'])
        if 'side_length' in request.form and request.form['side_length']:
            side_length = float(request.form['side_length'])
        if 'base_length' in request.form and request.form['base_length']:
            base_length = float(request.form['base_length'])
        if 'height' in request.form and request.form['height']:
            height = float(request.form['height'])

        volume_formula, _, volume = calculate_volume(shape, radius, side_length, base_length, height)
        label, value = get_label_and_value_for_shape(shape, radius, side_length, base_length, height)

        return render_template('index.html', shapes=['Sphere', 'Cube', 'Pyramid'], volume_formula=volume_formula, volume=volume, label=label, value=value)

    return render_template('index.html', shapes=['Sphere', 'Cube', 'Pyramid'])

if __name__ == '__main__':
    app.run(debug=True)
