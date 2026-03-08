"""ACEest Fitness & Gym - Flask Application."""

from flask import Flask, jsonify, request

app = Flask(__name__)

MEMBERS = [
    {"id": 1, "name": "Alice Johnson", "membership": "Gold", "age": 28},
    {"id": 2, "name": "Bob Smith", "membership": "Silver", "age": 35},
    {"id": 3, "name": "Charlie Davis", "membership": "Platinum", "age": 22},
    {"id": 4, "name": "Diana Ross", "membership": "Gold", "age": 30},
    {"id": 5, "name": "Ethan Hunt", "membership": "Silver", "age": 40},
]

CLASSES = [
    {"id": 1, "name": "Yoga Basics", "trainer": "Alice", "schedule": "Mon 8AM"},
    {"id": 2, "name": "HIIT Blast", "trainer": "Bob", "schedule": "Tue 6PM"},
    {"id": 3, "name": "Spin Cycle", "trainer": "Charlie", "schedule": "Wed 7AM"},
    {"id": 4, "name": "Strength Training", "trainer": "Diana", "schedule": "Thu 5PM"},
]


def calculate_bmi(weight_kg: float, height_m: float) -> dict:
    if height_m <= 0 or weight_kg <= 0:
        return {"error": "Weight and height must be positive numbers."}

    bmi = round(weight_kg / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {"bmi": bmi, "category": category}


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to ACEest Fitness & Gym!",
        "tagline": "Your journey to a healthier life starts here.",
        "status": "active"
    })


@app.route("/members")
def members():
    return jsonify({
        "members": MEMBERS,
        "total": len(MEMBERS)
    })


@app.route("/members/<int:member_id>")
def get_member(member_id):
    member = next((m for m in MEMBERS if m["id"] == member_id), None)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member)


@app.route("/classes")
def classes():
    return jsonify({
        "classes": CLASSES,
        "total": len(CLASSES)
    })


@app.route("/bmi")
def bmi():
    try:
        weight = float(request.args.get("weight", 0))
        height = float(request.args.get("height", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid weight or height value."}), 400

    result = calculate_bmi(weight, height)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)