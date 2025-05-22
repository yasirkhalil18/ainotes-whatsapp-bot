# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Health check route
@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running on Render!"

# Webhook route for Twilio
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    
    print(f"📩 Message from {from_number}: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()
    
    # Bot Response Logic
    if 'hello' in incoming_msg:
        msg.body("Hi there! 👋 This is AiNotes WhatsApp Bot.")
    elif 'notes' in incoming_msg:
        msg.body("📚 Visit https://AiNote.pk to get all educational notes!")
    else:
        msg.body("❓ Sorry, I didn't understand that. Type 'hello' to begin.")
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
