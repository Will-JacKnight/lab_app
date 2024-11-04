from flask import Flask, render_template, request
import re
import math
import requests
import os
# import json

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    GITHUB_UN = request.form.get("name")
    input_age = request.form.get("age")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    repos = []
    repo_response = requests.get(f"https://api.github.com/users/{GITHUB_UN}/repos", headers=headers)

    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        for repo in repo_data:
            repo_info = {
                "full_name": repo["full_name"],
                "html_url": repo["html_url"],
                "updated_at": repo["updated_at"],
                "description": repo["description"]
            }

            commits_response = requests.get(f"https://api.github.com/repos/{repo['full_name']}/commits", headers=headers)
            if commits_response.status_code == 200 and commits_response.json():
                latest_commit = commits_response.json()[0]  # Get the most recent commit
                repo_info["commit"] = {
                    "author": latest_commit["commit"]["author"]["name"],
                    "date": latest_commit["commit"]["author"]["date"],
                    "message": latest_commit["commit"]["message"]
                }
            else:
                repo_info["commit"] = {
                    "author": "Unknown",
                    "date": "Unknown",
                    "message": "No commit message available"
                }

            contributors_response = requests.get(f"https://api.github.com/repos/{repo['full_name']}/contributors", headers=headers)
            if contributors_response.status_code == 200 and contributors_response.json():
                contributors = contributors_response.json()
                contributors_list = []
                for contributor in contributors[:5]:
                    contributors_list.append({"login": contributor["login"],
                                              "contributions": contributor["contributions"]})
                repo_info["contributors"] = contributors_list
            else:
                repo_info["contributors"] = []

            repos.append(repo_info)

        return render_template("hello.html", name=GITHUB_UN, age=input_age, repos=repos)

    return "Response Error!"





@app.route("/query", methods=["GET"])
def query():
    query = request.args.get("q")
    return process_query(query)


def is_quare_and_cube(lt):
    new_lt = []
    for i in lt:
        square_root = int(math.sqrt(i))
        cube_root = round(abs(i) ** (1 / 3))
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
        integers = [int(num) for num in re.findall(r"\b\d+\b", query)]
        return str(max(integers))
    elif "plus" in query:
        summ = [int(num) for num in re.findall(r"\b\d+\b", query)]
        return str(sum(summ))
    elif "minus" in query:
        numbers = [int(num) for num in re.findall(r"\b\d+\b", query)]
        return str(numbers[0] - numbers[1])
    elif "both a square and a cube" in query:
        numbers = [int(num) for num in re.findall(r"\b\d+\b", query)]
        for num in numbers:
            root = round(num ** (1 / 6))  # 6th root check
            if root**2 == num ** (1 / 3) and root ** 3 == num ** (1 / 2):
                return num
            return "None found"
    elif "are primes" in query:
        numbers = [int(num) for num in re.findall(r"\d+", query)]
        primes = [num for num in numbers if is_prime(num)]
        return ", ".join(map(str, primes))
    elif "power":
        numbers = [int(num) for num in re.findall(r"\d+", query)]
        return str(numbers[0] ** numbers[1])
    else:
        return "This query is not within our test case."
