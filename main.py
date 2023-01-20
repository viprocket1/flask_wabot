from flask import Flask, request
from twilio.rest import Client
import os
import openai

app = Flask(__name__)

# OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


@app.route("/sms", methods=['POST'])
def sms():
  message_body = request.form['Body']
  phone_number = request.form['From']

  # Use the OpenAI API to generate a response
  response = openai.Completion.create(engine="text-davinci-002",
                                      prompt=f"{message_body}\n",
                                      max_tokens=2048)

  # Twilio account information
  account_sid = os.environ['TWILIO_ACCOUNT_SID']
  auth_token = os.environ['TWILIO_AUTH_TOKEN']
  client = Client(account_sid, auth_token)

  # Use the Twilio API to send a message
  message = client.messages.create(from_='whatsapp:+14155238886',
                                   body=response.choices[0].text,
                                   to=f'whatsapp:{phone_number}')

  return 'Response sent'


if __name__ == "__main__":
  app.run()
