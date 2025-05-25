# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search
import requests

app = Flask(__name__)

# Wit.ai API settings
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

    # Step 1: Detect intent via Wit.ai
    try:
        wit_response = requests.get(
            WIT_AI_URL + requests.utils.quote(incoming_msg),
            headers={"Authorization": f"Bearer {WIT_AI_TOKEN}"}
        )
        wit_data = wit_response.json()
        print("🧠 Wit.ai Response:", wit_data)

        intent = wit_data.get("intents", [{}])[0].get("name", "") if wit_data.get("intents") else ""
        print(f"🔍 Detected Intent: {intent}")

    except Exception as e:
        print("⚠️ Wit.ai Error:", e)
        msg.body("⚠️ I couldn't understand that. Please try again.")
        return str(resp)

    # Step 2: Intent-based AI response
    if intent == "greetings":
        msg.body("👋 Hello! I'm your AiNotes assistant.\nYou can ask for notes, textbooks or papers for FBISE, Punjab, Sindh, etc. 😊")
        return str(resp)

    elif intent in ["ask_notes", "ask_books", "study_help"]:
        # Use Google search to find the best result from ainotes.pk
        query = f"{incoming_msg} site:ainotes.pk"
        print(f"🔍 Searching Google for: {query}")

        try:
            results = list(search(query, num_results=1))
            if results:
                link = results[0]
                msg.body(f"📚 Here's what I found for:\n*{incoming_msg}*\n👉 {link}")
            else:
                msg.body("❌ Sorry! I couldn't find what you need. Please visit https://ainotes.pk directly.")
        except Exception as e:
            print("Google Search Error:", e)
            msg.body("⚠️ Something went wrong while searching. Please try again later.")
        return str(resp)

    else:
        msg.body("🤖 I'm still learning! Try asking for notes or say *hi* to start.")
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
