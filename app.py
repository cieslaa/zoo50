from flask import Flask, render_template, request, flash, redirect, url_for
from PIL import Image
from model import classify_image 
import os

# Configure app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure Flash
app.config["SECRET_KEY"] = os.urandom(24) 

@app.route("/", methods=["GET", "POST"])
def index():
    # If form sent ("POST")
    if request.method == "POST":
        
        if "animal_image" not in request.files:
            flash("No file found.", "error")
            return redirect(url_for("index")) 

        file = request.files["animal_image"]

        if file.filename == '':
            flash("No file selected.", "error")
            return redirect(url_for("index"))

        if file:
            try:
                img = Image.open(file.stream).convert("RGB")

                predictions = classify_image(img)

                return render_template('index.html', results=predictions)

            except Exception as e:
                print(f"Error processing image: {e}")
                flash(f"Error processing image: ({e})", "error")
                return redirect(url_for("index"))

    return render_template("index.html", results=None)


if __name__ == "__main__":
    app.run(debug=True)