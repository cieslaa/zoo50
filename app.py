from flask import Flask, render_template, request, session
from PIL import Image
from model import classify_image

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Main website
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Classify the animal based on the image
@app.route("/predict", methods=["POST"])
def predict():
    # No file sent in the form
    if "animal_image" not in request.files:
        return "No file found", 400
    
    file = request.files["animal_image"]

    # No file selected in the form
    if file.filename == '':
        return "No selected file", 400
    
    if file:
        try:
            # Use PIL module
            img = Image.open(file.stream)

            # Use the classify_image() function from model.py
            predictions = classify_image(img)

            return render_template('index.html', results=predictions)

        except Exception as e:
            print(f"Error processing image: {e}")
            return "Error processing image", 500


if __name__ == "__main__":
    app.run(debug=True)