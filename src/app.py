from flask import Flask, render_template, request
import re
import math

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


@app.route("/query", methods=["GET"])
def query():
    query = request.args.get("q")
    return process_query(query)


def is_quare_and_cube(lt):
    new_lt = []
    for i in lt:
        square_root = int(math.sqrt(i))
        cube_root = round(abs(i) ** (1/3))
        if square_root**2 == i and cube_root**3 == i:
            new_lt.append(i)
    return new_lt


def process_query(query):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif query == "asteroids":
        return "Unknown"
    elif query == "What is your name?":
        return "F4"
    elif "is the largest" in query:
        integers = [int(num) for num in re.findall(r'\b\d+\b', query)]
        return str(max(integers))
    elif "plus" in query:
        summ = [int(num) for num in re.findall(r'\b\d+\b', query)]
        return str(sum(summ))
    elif "minus" in query:
        numbers = [int(num) for num in re.findall(r'\b\d+\b', query)]
        return str(numbers[0]-numbers[1])
    elif "both a square and a cube" in query:
        numbers = [int(num) for num in re.findall(r'\b\d+\b', query)]
        for num in numbers:
            root = round(num ** (1 / 6)) # 6th root check
            if root ** 2 == num ** (1 / 3) and root ** 3 == num ** (1 / 2):
                return num
            return "None found"

    else:
        return "This query is not within our test case."
