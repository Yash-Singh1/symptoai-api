import json
read_file = open('message.txt').read()
yelp_json = json.loads(read_file)
yelp_values = yelp_json.values()
yelp_embeddings = []
for treatment in yelp_values:
  yelp_embeddings.append([treatment['text'], treatment['value']])
with open('Embeddings.txt', 'w') as file:
  file.write(json.dumps(yelp_embeddings))
print(yelp_embeddings)
