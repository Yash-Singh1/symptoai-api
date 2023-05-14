from flask import Flask, request
import requests
import json
import pinecone
import openai
import os
app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_KEY')
pinecone.init(
    environment=os.getenv('PINECONE_ENVIRONMENT'),
    api_key=os.getenv('PINECONE_API_KEY')
)
index = pinecone.Index('disease-symptoms')
@app.route('/query')
def query():
    sentence = request.args.get('sentence')
    xq = openai.Embedding.create(input=sentence, engine='text-embedding-ada-002')['data'][0]['embedding']
    result = index.query(xq, top_k=5, include_metadata=True, namespace='example-namespace')
    return json.dumps(eval(str(result)))
if __name__ == "__main__":
    app.run()