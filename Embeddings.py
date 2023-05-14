import openai
import pinecone
import json
from tqdm.auto import tqdm
openai.api_key = os.getenv('OPENAI_KEY')
pinecone.init(
    environment=os.getenv('PINECONE_ENVIRONMENT'),
    api_key=os.getenv('PINECONE_API_KEY')
)
index = pinecone.Index('dataset-of-diseases-and-symptoms')
string_data = open('Dataset.json', 'r').read()
dataset = json.loads(string_data)
dataset_symptoms = list(dataset.values())
dataset_diseases = list(dataset.keys())
for i in tqdm(range(0, len(dataset_symptoms), 32)):
    i_end = min(i+32, len(dataset_symptoms))
    symptoms_batch = dataset_symptoms[i: i+32]
    diseases_batch = dataset_diseases[i: i+32]
    ids_batch = [str(n) for n in range(i, i_end)]
    metadata = [{'metadata_key': disease} for disease in diseases_batch]
    result = openai.Embedding.create(input=symptoms_batch, engine='text-embedding-ada-002')
    embeds = [record['embedding'] for record in result['data']]
    to_upsert = zip(ids_batch, embeds, metadata)
    index.upsert(vectors=list(to_upsert), namespace='example-namespace')
