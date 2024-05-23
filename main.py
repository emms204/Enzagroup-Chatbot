from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/send_message', methods=['POST'])
def send_message():
    # Get the message from the POST data
    message = request.json['message']

    # Define the headers for the POST request
    headers = {
        'Content-Type': 'application/json',
    }

    # Define the data for the POST request
    data = {
        "sender": "user",
        "message": message
    }

    # Send the POST request to the Rasa server
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=json.dumps(data))

    # Return the response from the Rasa server
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
