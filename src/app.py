from flask import Flask, render_template, request
import re
import math
import requests
app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    GITHUB_UN = request.form.get("name")
    input_age = request.form.get("age")

    repo_list, last_updated_list = [], []
    response = requests.get(f"https://api.github.com/users/{GITHUB_UN}/repos")
    if response.status_code == 200:
        # data returned is a list of ‘repository’ entities
        repos = response.json()
        for repo in repos:
            # print(repo["full_name"])
            repo_list.append(repo["full_name"])
            last_updated_list.append(repo["updated_at"])

        return render_template("hello.html", name=GITHUB_UN, age=input_age,
                               repos=repos)
    return "Response Error!"


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

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

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
    elif "are primes" in query:
        numbers = [int(num) for num in re.findall(r'\d+', query)]
        primes = [num for num in numbers if is_prime(num)]
        return ", ".join(map(str, primes))
    elif "power":
        numbers = [int(num) for num in re.findall(r'\d+', query)]
        return str(numbers[0]**numbers[1])
    else:
        return "This query is not within our test case."
