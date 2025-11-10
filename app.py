from flask import Flask, request, jsonify
import joblib
import random
import json
import os

app = Flask(__name__)

# Load models
vectorizer = joblib.load("models/vectorizer.joblib")
classifier = joblib.load("models/classifier.joblib")

# Load intents safely
with open("data/intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"ok": True, "message": "College Helpdesk Bot API is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)
        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data["message"].strip().lower()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Vectorize input
        X = vectorizer.transform([user_message])
        predicted_tag = classifier.predict(X)[0]

        # Find responses
        for intent in intents:
            if intent["tag"] == predicted_tag:
                reply = random.choice(intent.get("responses", []))
                break
        else:
            reply = "Sorry, I didn’t understand that."

        return jsonify({
            "response": reply,
            "tag": predicted_tag
        })

    except Exception as e:
        # Return readable error for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Disable debug for production
    app.run(host="0.0.0.0", port=5000)
