from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Define a basic health check route
@app.route("/", methods=["GET"])
def home():
    return "AiNotes WhatsApp Bot is running ✅", 200

# Define webhook to handle incoming messages
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()

    if not incoming_msg:
        response.message("❌ I didn't receive any text. Please send a valid message.")
        return str(response)

    try:
        query = incoming_msg
        results = list(search(query, num_results=3))
        if results:
            reply = "🔎 Top search results for:\n" + query + "\n\n"
            for i, link in enumerate(results, 1):
                reply += f"{i}. {link}\n"
        else:
            reply = "⚠️ Sorry, I couldn't find any results."

    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    response.message(reply)
    return str(response)

# Run the app (if you want to run locally)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
