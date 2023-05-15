from flask import Flask, request
import json
import pinecone
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_KEY')
pinecone.init(
    environment=os.getenv('PINECONE_ENVIRONMENT'),
    api_key=os.getenv('PINECONE_API_KEY')
)
index = pinecone.Index('dataset-of-diseases-and-symptoms')
@app.route('/query')
def query():
    sentence = request.args.get('sentence')
    xq = openai.Embedding.create(input=sentence, engine='text-embedding-ada-002')['data'][0]['embedding']
    result = index.query(xq, top_k=5, include_metadata=True, namespace='example-namespace')
    return json.dumps(eval(str(result)))
if __name__ == "__main__":
    app.run()
