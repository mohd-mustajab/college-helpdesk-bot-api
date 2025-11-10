from http.server import BaseHTTPRequestHandler
import json
import requests
import os

# Environment variable for security
BOT_TOKEN = os.getenv("BOT_TOKEN")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            # Extract message and chat ID
            message = data.get("message", {}).get("text", "")
            chat_id = data.get("message", {}).get("chat", {}).get("id", "")

            if message and chat_id:
                # Send the message to the internal Flask backend (/chat)
                backend_url = f"https://college-helpdesk-bot-api.vercel.app/chat"
                res = requests.post(backend_url, json={"message": message})

                if res.status_code == 200:
                    bot_reply = res.json().get("response", "Sorry, I didn’t understand that.")
                else:
                    bot_reply = f"⚠️ Backend error {res.status_code}"
            else:
                bot_reply = "❌ No message found."

            # Send the reply back to Telegram
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": bot_reply}
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode("utf-8"))

    def do_GET(self):
        # Simple check endpoint
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "message": "Telegram webhook is active!"}).encode("utf-8"))
