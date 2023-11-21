from flask import Flask, render_template, request
from owlready2 import get_ontology, Thing, Property, restriction, has, sync_reasoner

app = Flask(__name__)

# Load the ontology
onto_path.append("path/to/your/ontology")  # Replace with the actual path
onto = get_ontology("http://example.org/your-ontology.owl").load()

# Define classes for shapes and volume calculations
class Shape(Thing):
    pass

class VolumeCalculation(Thing):
    pass

class ShapeHasVolume(Property):
    domain = [Shape]
    range = [VolumeCalculation]

# Define specific shapes with volume calculation requirements
class Sphere(Shape):
    equivalent_to = [Shape & restriction(ShapeHasVolume, some = [VolumeCalculation])]
    
class Cube(Shape):
    equivalent_to = [Shape & restriction(ShapeHasVolume, some = [VolumeCalculation])]

class Pyramid(Shape):
    equivalent_to = [Shape & restriction(ShapeHasVolume, some = [VolumeCalculation])]

# Create volume calculation functions
def sphere_volume(radius):
    return (4/3) * 3.14 * radius**3

def cube_volume(side_length):
    return side_length**3

def pyramid_volume(base_length, height):
    return (1/3) * base_length**2 * height

# Create volume calculation instances with specific requirements
calculation1 = VolumeCalculation(name="Calculation1", has=[Sphere], formula=sphere_volume)
calculation2 = VolumeCalculation(name="Calculation2", has=[Cube], formula=cube_volume)
calculation3 = VolumeCalculation(name="Calculation3", has=[Pyramid], formula=pyramid_volume)

# Save changes
sync_reasoner()
onto.save()

# Define Flask routes and views
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        shape_name = request.form['shape']
        radius = float(request.form['radius'])
        side_length = float(request.form['side_length'])
        base_length = float(request.form['base_length'])
        height = float(request.form['height'])

        # Get the selected shape from ontology
        selected_shape = getattr(onto, shape_name)

        # Retrieve the corresponding volume calculation
        volume_calculation = selected_shape.is_a[0].has[0]

        # Calculate the volume
        volume = volume_calculation.formula(radius=radius, side_length=side_length, base_length=base_length, height=height)

        # LaTeX steps for calculation
        latex_steps = [
            f"1. Outlining the inputs: {', '.join([f'{param}={value}' for param, value in [('radius', radius), ('side', side_length), ('base', base_length), ('height', height)]])}",
            f"2. Writing the formula to be used: {volume_calculation.formula.__doc__}",
            f"3. Illustrating the substitutions: {volume_calculation.formula.__doc__.format(radius=radius, side_length=side_length, base_length=base_length, height=height)}",
            f"4. Finally showing the answer: {volume}"
        ]

        return render_template('index.html', shapes=['Sphere', 'Cube', 'Pyramid'], latex_steps=latex_steps)

    return render_template('index.html', shapes=['Sphere', 'Cube', 'Pyramid'])

if __name__ == '__main__':
    app.run(debug=True)
