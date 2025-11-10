from http.server import BaseHTTPRequestHandler
import json
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode("utf-8"))

        message = data.get("message", {}).get("text", "")
        chat_id = data.get("message", {}).get("chat", {}).get("id", "")

        if message and chat_id:
            try:
                # since backend is in same repo, just call the internal endpoint
                res = requests.post("https://college-helpdesk-bot.vercel.app/chat", json={"message": message})
                if res.status_code == 200:
                    reply = res.json().get("response", "Sorry, I didn’t understand that.")
                else:
                    reply = f"⚠️ API error {res.status_code}"
            except Exception as e:
                reply = f"❌ Could not reach backend: {e}"

            # Send the response back to Telegram
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": reply},
            )

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "message": "Webhook is active"}).encode("utf-8"))
