from flask import Flask, request, jsonify
import joblib, json, random, datetime, csv, os
import numpy as np

app = Flask(__name__)

# Load models and intents
vect = joblib.load("models/vectorizer.joblib")
clf = joblib.load("models/classifier.joblib")
intents = json.load(open("data/intents.json", "r", encoding="utf-8"))

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

def get_responses_for_tag(tag):
    for it in intents["intents"]:
        if it["tag"] == tag:
            return it.get("responses", [])
    return []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    x = vect.transform([message])
    probs = clf.predict_proba(x)[0]
    idx = np.argmax(probs)
    tag = clf.classes_[idx]
    prob = float(probs[idx])

    if prob < 0.5:
        tag = "fallback"

    responses = get_responses_for_tag(tag)
    resp = random.choice(responses) if responses else "Sorry, I don't know that."

    # Log chat
    with open("logs/chats.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.utcnow().isoformat(), message, resp, tag, prob])

    return jsonify({
        "response": resp,
        "tag": tag,
        "confidence": prob
    })

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "College Helpdesk API is running 🚀"})

if __name__ == "__main__":
    app.run(debug=True)
