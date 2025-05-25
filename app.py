# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search
import requests  # For Wit.ai API

app = Flask(__name__)

# Wit.ai API Settings
WIT_AI_TOKEN = "4JQVXVMJ5M5EEEHGI3XJNCMUKTXCXE4H"
WIT_AI_URL = "https://api.wit.ai/message?v=20250525&q="

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    # Step 1: Call Wit.ai API to understand the message
    try:
        wit_response = requests.get(
            WIT_AI_URL + requests.utils.quote(incoming_msg),
            headers={"Authorization": f"Bearer {WIT_AI_TOKEN}"}
        )
        wit_data = wit_response.json()
        print("🧠 Wit.ai Response:", wit_data)
    except Exception as e:
        print("⚠️ Wit.ai Error:", e)
        msg.body("⚠️ Error understanding your message. Please try again.")
        return str(resp)

    # Step 2: Continue with Google Search on ainotes.pk
    query = f"{incoming_msg} site:ainotes.pk"
    print(f"🔍 Searching Google for: {query}")

    try:
        results = list(search(query, num_results=1))
        if results:
            link = results[0]
            msg.body(f"🔗 Here's what I found for:\n*{incoming_msg}*\n👉 {link}")
        else:
            msg.body("❌ Sorry! I couldn't find the link. Try visiting https://ainotes.pk directly.")
    except Exception as e:
        msg.body("⚠️ Error fetching result. Please try again later.")
        print("Google Search Error:", e)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
