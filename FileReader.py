import os
import json
files = os.listdir('Symptoms/')
dataset = {}
file_num = 0
for disease in files:
  file_num += 1
  file_dis = open('Symptoms/' + disease, 'r')
  lines = file_dis.readlines()
  thread_symptoms = ''
  thread_diseases = ''
  for line in lines:
    if '* ' in line:
      new_line = line.split('* ')[1]
      thread_symptoms += new_line
    elif '# ' in line:
      if "## " in line:
        pass
      else:
        new_line = line.split('# ')[1]
        thread_diseases += new_line
    else:
      pass
  dataset[thread_diseases] = thread_symptoms
unique_dataset = {}
for key, value in dataset.items():
    if value not in unique_dataset.values():
        unique_dataset[key] = value
print(unique_dataset)
with open('Dataset.json', 'w') as file_data:
  data = json.dumps(unique_dataset)
  file_data.write(data)
