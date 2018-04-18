from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "HELLO MY DUDES";

@app.route("/sentiment", methods=['POST'])
def sentiment():
    body = request.get_json()
    if 'text' not in body:
        response = jsonify({ "message": "Bad request" })
        response.status_code = 400
        return response
    
    text = body['text']
    blob = TextBlob(text)
    response = [
        {
            'text': str(sentence),
            'sentiment': sentence.sentiment.polarity
        } for sentence in blob.sentences
    ]

    response = jsonify(response)

    return response
