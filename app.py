from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot_train import get_response
from twilio.rest import Client
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    
    # Create reply
    resp = MessagingResponse()
    reply=get_response(msg)
    resp.message("Solution: {}".format(reply))
    return str(resp)



@app.route("/sendmedia", methods=['POST'])
def send_media():
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'ACa5dc979d2cddc016a19b6d65b1044e35'
    auth_token = '3f1c0487c13fe753eb47954e9b6606ca'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            media_url=['https://drive.google.com/uc?export=download&id=15gRZAuVFEk1MHtWKMvho6MN4lLIOsc1H'],
            from_='whatsapp:+14155238886',
            body="It's taco time!",
            to='whatsapp:+917738560715'
        )

    print(message.sid)
    return str(message)
if __name__ == "__main__":
    app.run(debug=True)
