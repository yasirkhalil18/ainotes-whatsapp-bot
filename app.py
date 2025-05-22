from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()

    # Basic keyword extraction
    if 'class' in incoming_msg and 'chemistry' in incoming_msg and 'fbise' in incoming_msg:
        reply = "https://ainotes.pk/class-9-notes-pdf-chemistry-federal-board-fbise/"
    else:
        reply = "Notes hasail krny k leay class, subject or board likhy. Admin k reply k leay wait kryn."

    # Twilio response
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    return str(resp)

if __name__ == '__main__':
    app.run()
