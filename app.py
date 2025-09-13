from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bmi", methods=["POST"])
def bmi():
    try:
        weight = float(request.form.get("weight", 0))
        height = float(request.form.get("height", 0))
        unit = request.form.get("unit", "metric")
        
        if unit == "metric":
            bmi_value = round(weight / ((height / 100) ** 2), 2)
        elif unit == "imperial":
            bmi_value = round((weight / (height * height)) * 703, 2)
        else:
            bmi_value = "Invalid unit"

        if bmi_value < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi_value < 25:
            category = "Fit"
        else:
            category = "Overweight"

        return render_template("index.html", bmi=bmi_value, category=category)
    except Exception:
        return render_template("index.html", bmi="Invalid input", category="")

# FitBot endpoint
@app.route("/fitbot", methods=["POST"])
def fitbot():
    data = request.get_json()
    message = data.get("message", "")
    category = data.get("category", "")
    
    # Initial greeting
    if message == "start":
        response = "Hi, I’m FitBot. I can guide you based on your BMI. Which category do you belong to?"
        options = ["Underweight", "Fit", "Overweight"]
        return jsonify({"response": response, "options": options, "category": ""})
    
    # Set category
    if category == "" and message in ["Underweight", "Fit", "Overweight"]:
        response = f"Great! You selected {message}. What do you want to know?"
        options = ["Meal Plans", "Workouts", "Key Suggestions", "Thank FitBot"]
        return jsonify({"response": response, "options": options, "category": message})

    # Handle topic selection
    if message in ["Meal Plans", "Workouts", "Key Suggestions"]:
        content = {
            "Meal Plans": "Include balanced meals with proteins, carbs, and healthy fats.",
            "Workouts": "Combine cardio, strength, and flexibility exercises weekly.",
            "Key Suggestions": "Stay hydrated, sleep well, and maintain consistency in routines."
        }
        response = content.get(message, "")
        options = ["Meal Plans", "Workouts", "Key Suggestions", "Thank FitBot"]
        return jsonify({"response": response, "options": options, "category": category})

    if message == "Thank FitBot":
        response = "You’re welcome! Stay healthy and fit!"
        return jsonify({"response": response, "options": [], "category": ""})

    return jsonify({"response": "I didn't understand. Please select an option.", "options": [], "category": category})

if __name__ == "__main__":
    app.run(debug=True)
