from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
from pythonosc import udp_client

app = Flask(__name__)
CORS(app)

def send_osc(endpoint, msg='ping'):
    client = udp_client.SimpleUDPClient('127.0.0.1', 12345)
    try:
        client.send_message(endpoint, msg)
    except:
        print "There was an error contacting the OSC server, is it up and running on " + "127.0.0.1:12345"

@app.route('/')
def hello():
    return "HELLO MY DUDES"



@app.route("/sentiment", methods=['POST'])
def sentiment():
    body = request.get_json()
    if 'text' not in body:
        response = jsonify({ "message": "Bad request" })
        response.status_code = 400
        return response
    
    text = body['text']
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    # Notify the osc-server
    send_osc('/Sentiment', sentiment)

    response =  {
            'text': text,
            'sentiment': sentiment
        }


    response = jsonify(response)

    return response

@app.route('/Recording/start', methods=['POST'])
def start():
    send_osc('/Recording/start')
    return ('', 204)

@app.route('/Recording/end', methods=['POST'])
def end():
    send_osc('/Recording/end')
    return ('', 204)