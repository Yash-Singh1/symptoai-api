import os
import json
files = os.listdir('Symptoms/')
dataset_symptoms = []
dataset_diseases = []
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
  dataset_symptoms.append(thread_symptoms)
  dataset_diseases.append(thread_diseases)
with open('Symptoms.txt', 'w') as txt_symp:
  txt_symp.write(str(dataset_symptoms))
with open('Diseases.txt', 'w') as txt_dise:
  txt_dise.write(str(dataset_diseases))