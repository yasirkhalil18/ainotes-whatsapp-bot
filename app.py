# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search  # uses Google Custom Search

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    query = f"{incoming_msg} site:ainotes.pk"
    print(f"🔍 Searching Google for: {query}")

    try:
        results = list(search(query, num_results=1))  # Only top result
        if results:
            link = results[0]
            msg.body(f"🔗 Here's what I found for:\n*{incoming_msg}*\n👉 {link}")
        else:
            msg.body("❌ Sorry! I couldn't find the link. Try visiting https://ainotes.pk directly.")
    except Exception as e:
        msg.body("⚠️ Error fetching result. Please try again later.")
        print("Error:", e)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
