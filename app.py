# app.py

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📨 Incoming Data:", data)

    # Aap yahan apna WhatsApp bot ka logic laga saktay ho
    return {"status": "received"}, 200

if __name__ == "__main__":
    app.run(debug=True)
