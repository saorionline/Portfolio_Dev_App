import json
from pathlib import Path

from django.shortcuts import render

DATA_DIR = Path(__file__).resolve().parent / "data"


def load(name):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def dashboard(request):
    courses = load("curriculum.json")
    for course in courses:
        lessons = [lesson for module in course["modules"] for lesson in module["lessons"]]
        course["total"] = len(lessons)
        course["done"] = sum(1 for lesson in lessons if lesson.get("done"))

    return render(request, "portfolio/dashboard.html", {
        "projects": load("projects.json"),
        "courses": courses,
        "capsules": load("portfolio.json"),
    })
