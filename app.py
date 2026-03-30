"""
app.py — servidor Flask E-BOT LITE 🦙
"Llama que llama... por wasap"
"""

import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from handlers import procesar

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "🦙 E-BOT LITE — OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    numero = request.form.get("From", "")
    body   = request.form.get("Body", "").strip()
    resp   = MessagingResponse()
    procesar(numero, body, resp)
    return str(resp), 200, {"Content-Type": "text/xml"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
