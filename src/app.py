from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)

@app.route("/page")
def page():
    return "Welcome to page!"

# flask --app app.py run --host=0.0.0.0 --port 8000/homes/jw1524/modules/SSE/website/index.html
# debug mode: flask --app example --debug run
