from flask import Flask, request, jsonify
import joblib
import random
import json
import os

app = Flask(__name__)

# Load models
vectorizer = joblib.load("models/vectorizer.joblib")
classifier = joblib.load("models/classifier.joblib")

# Load intents
with open("data/intents.json", "r") as f:
    intents = json.load(f)["intents"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "College Helpdesk Bot API is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").lower()

        # Vectorize user input
        X = vectorizer.transform([user_message])
        tag = classifier.predict(X)[0]

        # Find responses
        for intent in intents:
            if intent["tag"] == tag:
                return jsonify({"reply": random.choice(intent["responses"])})

        # Fallback
        return jsonify({"reply": "Sorry, I didn’t understand that."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
