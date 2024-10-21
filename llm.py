import os
import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Accessing the variables
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
with open('restaurant.json', 'r', encoding='utf-8') as file:
    data = file.read()

template = os.getenv("PROMPT")

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/chat', methods=['POST'])
@cross_origin()
def chat_completion():
    user_input = request.json.get('text', '')
    if not user_input:
        return jsonify({'error': 'No text provided'}), 400

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
            {
                "role": "system",
                "content": "Olá como posso ajuda-lo hoje?" 
            },
            {
                "role": "user",
                "content": data,
            },
            {
                "role": "system",
                "content": "Entendi, como esta seu apetite hoje? diga-me o que deseja para que eu consiga lhe ajudar a escolher"
            }
        ],
        model="llama3-8b-8192",
    )

    return jsonify({'response': chat_completion.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
