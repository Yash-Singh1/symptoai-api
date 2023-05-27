from flask import Flask, request
import openai
from flask_cors import CORS
import os
import json
import pinecone
import tiktoken
import redis

r = redis.Redis(
  host= 'usw1-superb-kite-34403.upstash.io',
  port= '34403',
  password= os.getenv('REDIS_PASSWORD'),
)

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv('OPENAI_KEY')
prompt = 'You are a helpful assistant that does the following: Your main job will be to provide the top 5\
  medical issues, problems or conditions based on user information provided. The user information will be in\
  a dictionary. This dictionary will consist of variables, such as age, sex, symptoms, past medical history, \
  current injury/trauma to the area, medications, and lifestyle factors. Your output will also be in the form\
  of a dictionary consist of the top 5 medical issues, conditions, or problems the user could be having, and\
  corresponding to them, you will provide another dictionary, which will consist of the probability that the\
  user could be experiencing, listed with one of the five "Very High, High, Moderate, Low, Very Low". You will\
  also provide a 20-30 word summary of each of the medical issues, problems or conditions, in that dictionary.\
  Finally, you will also provide what kind of doctor or treatment they should see, in 1-3 words in that\
  Dictionary. The specialist doctor can be the same across all issues but does not have to be. The only output you\
  will return is the dictionary, which should adhere to the JSON spec.'
example_info = '{"age":15,"sex":"male","symptoms":"pain in the wrist, inability of motion near the wrist",\
  "recent injury/trauma to the area":"got hit with a soccer ball at a high speed, in the wrist",\
  "past medical issues":"fractured same wrist two years ago, in an injury, took two months to\
  heal","lifestyle/medications":"plays a lot of soccer, eats well, takes vitamin D3"}'
example_answer = '{"Wrist sprain/strain":{"probability":"Very High","summary":"Stretching or tearing of wrist\
  ligaments due to sudden force or excessive bending, leading to pain and limited motion.", "treatment": "Orthopedic\
  Doctor"},"Wrist fracture": {"probability":"Moderate","summary":"A break in the bones of the wrist, which may\
  occur from trauma or re-injury, causing pain, swelling, and difficulty moving the wrist."},"Ligament Tear":\
  {"probability":"Moderate","summary":"Damage to the ligaments in the wrist, often caused by trauma, leading\
  to pain, instability, and compromised wrist function.", "treatment": "Orthopedic Doctor"},"Tendonitis":\
  {"probability":"Low","summary":"Inflammation of the tendons in the wrist, typically caused by repetitive or \
  excessive use, resulting in pain and restricted movement.", "treatment": "Orthopedic Doctor"},"Arthritis":\
  {"probability":"Very Low","summary":"Inflammation of the joints in the wrist, which can occur at a young age\
  as well, causing pain, stiffness, and limited range of motion.", "treatment": "Rheumatologists"}}'
pinecone.init(
    environment=os.getenv('PINECONE_ENV'),
    api_key=os.getenv("PINECONE_KEY")
)

index = pinecone.Index('dataset-of-yelp-embeddings')
@app.route('/query')
def query():
    # We already have redis based verification
    # if request.headers.get('Authorization') != os.getenv('API_KEY'):
    #     return '{ "error": "Unauthenticated" }', 401
    if request.headers.get('X-SymptoAI-Auth') is None:
        return '{ "error": "Unauthenticated" }', 401
    if r.get(request.headers.get('X-SymptoAI-Auth')) is None:
        return '{ "error": "Unauthenticated" }', 401
    r.delete(request.headers.get('X-SymptoAI-Auth'))
    user_info = request.args.get('user_info')
    query_returns = []
    message = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": example_info},
                {"role": "assistant", "content": example_answer},
                {"role": "user", "content": user_info}
          ]
      )
    dictionary = json.loads(message['choices'][0]['message']['content'])
    resources = []
    queries = []
    for _condition, info in dictionary.items():
        treatment = info["treatment"]
        resources.append(treatment)
    for vector in resources:
        treatment_vectors = openai.Embedding.create(input=vector, engine='text-embedding-ada-002')['data'][0]['embedding']
        results = index.query(treatment_vectors, top_k=5, include_metadata=True, namespace='example-namespace')
        queries.append(results)
    for num in range(5):
        match_string = queries[num]['matches'][0]['metadata']['metadata_key']
        query_returns.append(match_string)
    count = 0
    for key, value in dictionary.items():
        dictionary[key].update({"metadata": query_returns[count]})
        count += 1
    return json.dumps(dictionary)

enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

@app.route('/count')
def count():
    return json.dumps(len(enc.encode(request.args.get('text'))))

if __name__ == "__main__":
    app.run()
