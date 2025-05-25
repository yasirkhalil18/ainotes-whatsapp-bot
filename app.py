from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from transformers import pipeline
from googlesearch import search
import requests

app = Flask(__name__)
classifier = pipeline("zero-shot-classification")

candidate_labels = [
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

fallback_keywords = ["textbook", "notes", "pma", "css", "pms", "roadmap", "lab", "practical", "mdcat", "mcqs", "past papers"]

@app.route("/", methods=["GET"])
def index():
    return "WhatsApp Bot Running!"

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    # NLP intent detection
    result = classifier(incoming_msg, candidate_labels)
    intent = result['labels'][0]

    # Fallback keyword detection
    for word in fallback_keywords:
        if word in incoming_msg.lower():
            intent = word
            break

    # Google search with site limiter
    search_query = f"{incoming_msg} site:ainotes.pk"
    search_results = list(search(search_query, num_results=3))

    if search_results:
        response_text = f"🔎 Top results from AiNotes.pk for '{incoming_msg}':\n"
        for url in search_results:
            response_text += f"\n👉 {url}"
    else:
        response_text = "Sorry! No matching content found on AiNotes.pk. Try different keywords."

    msg.body(response_text)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
