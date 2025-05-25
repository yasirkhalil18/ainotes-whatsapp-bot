from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HF_HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"
}

# ✅ Updated candidate labels
def classify_intent(text):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": [
                "textbook", "textbooks", "notes", "class notes", "chapter wise notes", "solved notes",
                "past papers", "guess papers", "helping notes", "MCQs", "short questions", "long questions",
                "solved exercises", "lab manual", "practical notebook", "biology practical", "chemistry practical",
                "physics practical", "army test notes", "pma notes", "issb notes", "css notes", "pms notes",
                "entry test notes", "mdcat notes", "ecat notes", "nums notes",
                "9th class notes", "10th class notes", "1st year notes", "2nd year notes", "matric notes",
                "intermediate notes", "FBISE notes", "Punjab board notes", "Sindh board notes",
                "KPK board notes", "Balochistan board notes", "AJK board notes",
                "python roadmap", "java notes", "sql notes", "coding roadmap",
                "ai roadmap", "web development notes"
            ]
        }
    }
    try:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)
        result = response.json()
        label = result['labels'][0]
        return label
    except Exception as e:
        print("NLP Error:", e)
        return "unknown"

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    intent = classify_intent(incoming_msg)
    print(f"Detected intent: {intent}")

    if intent == "notes":
        query = f"{incoming_msg} site:ainotes.pk"
    elif intent == "army test notes":
        # Army specific notes search keywords
        army_keywords = ["basai notes", "kpma notes", "pms notes", "army test notes", "pak army notes"]
        matched = [k for k in army_keywords if k in incoming_msg]
        if matched:
            query = f"{matched[0]} site:ainotes.pk"
        else:
            query = f"army notes site:ainotes.pk"
    elif intent == "greeting":
        msg.body("👋 Hello! I can help you find class notes, Army test notes, and more from ainotes.pk. Try typing '10th Chemistry notes' or 'Basai notes'.")
        return str(resp)
    elif intent == "bye":
        msg.body("👋 Goodbye! See you again soon.")
        return str(resp)
    elif intent == "help":
        msg.body("ℹ️ Send me a subject or exam name like '9th Physics notes', 'Basai notes', or 'PMS notes', and I'll find them from ainotes.pk.")
        return str(resp)
    else:
        msg.body("🤖 Sorry, I didn’t understand that. Try sending something like 'Class 9 Biology' or 'Army test notes'.")
        return str(resp)

    try:
        results = list(search(query, num_results=1))
        if results:
            msg.body(f"📘 Here's what I found for:\n*{incoming_msg}*\n🔗 {results[0]}")
        else:
            msg.body("❌ Sorry! Couldn't find related notes. Please try again or visit https://ainotes.pk directly.")
    except Exception as e:
        print("Google Search Error:", e)
        msg.body("⚠️ Something went wrong with the search. Please try again later.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
