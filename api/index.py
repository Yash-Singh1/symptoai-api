from flask import Flask, request
import json
import pinecone
import openai
import os
from flask_cors import CORS
app = Flask(__name__)
import time
CORS(app)
openai.api_key = os.getenv('OPENAI_KEY')
pinecone.init(
    environment=os.getenv('PINECONE_ENVIRONMENT'),
    api_key=os.getenv('PINECONE_API_KEY')
index = pinecone.Index('dataset-of-diseases-and-symptoms')
@app.route('/query')
def query():
    chat_gpt_returns = []
    sentence = request.args.get('sentence')
    xq = openai.Embedding.create(input=sentence, engine='text-embedding-ada-002')['data'][0]['embedding']
    results = index.query(xq, top_k=5, include_metadata=True, namespace='example-namespace')
    for num in range(5):
        message = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that given a medical conditions, output what specialist doctor they should go to, and the output should be 1 word."},
                {"role": "user", "content": "Heart pain"},
                {"role": "assistant", "content": "Cardiologist"},
                {"role": "user", "content": "Leg fracture"},
                {"role": "assistant", "content": "Orthopedist"},
                {"role": "user", "content": results['matches'][num]['metadata']['metadata_key']}
            ]
        )
        output = message.get('choices')[0]
        content = output.get('message')
        response = content.get('content') #OUTPUT FROM BACK-END
        chat_gpt_returns.append(response)
    return str(chat_gpt_returns)
if __name__ == "__main__":
    app.run()

