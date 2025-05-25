# app.py

import os
from dotenv import load_dotenv
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Hugging Face API Config
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HF_HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"
}

def classify_intent(text):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": ["notes", "greeting", "bye", "help"]
        }
    }
    try:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        label = result['labels'][0]  # Top predicted label
        return label
    except Exception as e:
        print("❌ NLP Error:", e)
        return "unknown"

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    intent = classify_intent(incoming_msg)
    print(f"🧠 Intent detected: {intent}")

    if intent == "notes":
        query = f"{incoming_msg} site:ainotes.pk"
        try:
            results = list(search(query, num_results=1))
            if results:
                link = results[0]
                msg.body(f"📘 Here's what I found for:\n*{incoming_msg}*\n🔗 {link}")
            else:
                msg.body("❌ Sorry! Couldn't find notes. Try visiting https://ainotes.pk.")
        except Exception as e:
            print("❌ Google Search Error:", e)
            msg.body("⚠️ Something went wrong. Please try again later.")

    elif intent == "greeting":
        msg.body("👋 Hello! I can help you find class notes from ainotes.pk. Just type something like:\n*9th class Physics notes*")

    elif intent == "bye":
        msg.body("👋 Goodbye! See you again soon.")

    elif intent == "help":
        msg.body("ℹ️ Send me a subject or class (e.g. '10th Chemistry notes') and I'll find it for you from ainotes.pk.")

    else:
        msg.body("🤖 Sorry, I didn’t understand that. Please send a class + subject name (e.g. 'Class 9 Biology').")

    return str(resp)

if __name__ == "__main__":
    # For development use only. Use gunicorn for production.
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
