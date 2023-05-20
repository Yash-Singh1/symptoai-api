import openai
import pinecone
import json
from tqdm.auto import tqdm
import os
openai.api_key = os.getenv('OPENAI_KEY')
pinecone.init(
    environment=os.getenv('PINECONE_ENV'),
    api_key=os.getenv('PINECONE_KEY')
)
index = pinecone.Index('dataset-of-yelp-embeddings')
string_data = open('Embeddings.json', 'r').read()
dataset = json.loads(string_data)
for i in tqdm(range(0, len(dataset), 34)):
    i_end = min(i+34, len(dataset))
    batch = [data[0] for data in dataset[i: i+34]]
    print(batch)
    other_batch = dataset[i: i+34]
    ids_batch = [str(n) for n in range(i, i_end)]
    metadata = [{'metadata_key': key} for key in other_batch]
    result = openai.Embedding.create(input=batch, engine='text-embedding-ada-002')
    embeds = [record['embedding'] for record in result['data']]
    to_upsert = zip(ids_batch, embeds, metadata) 
    index.upsert(vectors=list(to_upsert), namespace='example-namespace')
