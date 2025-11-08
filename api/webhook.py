from flask import Flask, request
import requests, os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

@app.route("/api/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return {"ok": True}  # ignore non-message updates

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    # Send text to your backend (the Flask app)
    try:
        res = requests.post(API_URL, json={"message": text})
        if res.status_code == 200:
            bot_reply = res.json().get("response", "Sorry, I didn't understand that.")
        else:
            bot_reply = f"⚠️ Server error {res.status_code}"
    except Exception as e:
        bot_reply = f"❌ API unreachable: {e}"

    # Send reply back to user
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
        "chat_id": chat_id,
        "text": bot_reply
    })
    return {"ok": True}

if __name__ == "__main__":
    app.run()
