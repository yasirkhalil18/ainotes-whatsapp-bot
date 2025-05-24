# app.py

import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Load the JSON data (once)
with open("search-data.json", "r") as f:
    data = json.load(f)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower().strip()
    from_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    # Simple search: check if query in title
    found = None
    for item in data:
        if incoming_msg in item['title'].lower():
            found = item
            break

    if found:
        msg.body(f"🔗 Here's what I found for:\n*{incoming_msg}*\n👉 {found['link']}")
    else:
        msg.body("❌ Sorry! I couldn't find any link. Try different words or visit https://ainotes.pk")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
