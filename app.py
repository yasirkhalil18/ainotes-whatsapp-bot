from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    
    print(f"📨 Message from {from_number}: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()
    
    # Simple auto-reply logic
    if 'hello' in incoming_msg:
        msg.body("Hi there! 👋 This is AiNotes WhatsApp Bot.")
    else:
        msg.body("Sorry, I didn't understand that. Type 'hello' to begin.")
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
