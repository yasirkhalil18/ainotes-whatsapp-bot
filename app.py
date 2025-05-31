from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEEPSEEK_API_KEY = "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"

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot with DeepSeek is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    greeting_keywords = ["hello", "hi", "hey", "salam", "assalamualaikum"]
    if any(word in incoming_msg.lower() for word in greeting_keywords):
        msg.body("👋 Hello! I can help you find class notes, Army test notes, and more from ainotes.pk. Try typing '10th Chemistry notes' or 'Basai notes'.")
        return str(resp)

    if any(word in incoming_msg.lower() for word in ["bye", "goodbye", "khuda hafiz"]):
        msg.body("👋 Goodbye! See you again soon.")
        return str(resp)

    if "help" in incoming_msg.lower():
        msg.body("ℹ️ Send me a subject or exam name like '9th Physics notes', 'Basai notes', or 'PMS notes', and I'll find them from ainotes.pk.")
        return str(resp)

    query = f"{incoming_msg} site:ainotes.pk"

    try:
        results = list(search(query, num_results=1))
        if results:
            msg.body(f"📘 Here's what I found for:\n*{incoming_msg}*\n🔗 {results[0]}")
        else:
            # Fallback to DeepSeek if Google search fails
            deepseek_payload = {
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an educational assistant that helps students find academic notes and answers from Ainotes.pk"
                    },
                    {
                        "role": "user",
                        "content": f"{incoming_msg}"
                    }
                ]
            }
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            r = requests.post(DEEPSEEK_API_URL, headers=headers, json=deepseek_payload)
            if r.status_code == 200:
                result = r.json()
                reply = result['choices'][0]['message']['content']
                msg.body(f"🤖 DeepSeek Reply:\n{reply}")
            else:
                msg.body("⚠️ No results found via Google or DeepSeek.")
    except Exception as e:
        print("Search/DeepSeek Error:", e)
        msg.body("⚠️ Something went wrong. Please try again later.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
