import openai
import pinecone
import json
from tqdm.auto import tqdm
openai.api_key = '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'
pinecone.init(
    environment="asia-southeast1-gcp-free" ,
    api_key="4715666f-7009-4cb6-8857-9dae917a2e75"
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
