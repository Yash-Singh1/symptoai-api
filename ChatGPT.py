#Import modules, and set up flask server
from flask import Flask, request
import openai
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv('OPENAI_KEY') #API Key
#Variables
prompt = 'You are a helpful assistant that does the following: Your main job will be to provide the top 5\
  medical issues, problems or conditions based on user information provided. The user information will be in\
  a dictionary. This dictionary will consist of variables, such as age, sex, symptoms, past medical history, \
  current injury/trauma to the area, medications, and lifestyle factors. Your output will also be in the form\
  of a dictionary consist of the top 5 medical issues, conditions, or problems the user could be having, and\
  corresponding to\ them, you will provide another dictionary, which will consist of the probability that the\
  user could be experiencing, listed with one of the five "Very High, High, Moderate, Low, Very Low". You will\
  also provide a 20-30 word summary of each of the medical issues, problems or conditions, in that dictionary.\
  The only output you will return is the dictionary.'
example_info = '{"age":15,"sex":"male","symptoms":"pain in the wrist, inability of motion near the wrist",\
  "recent injury/trauma to the area":"got hit with a soccer ball at a high speed, in the wrist","medications":\
  "vitamin D3","past medical issues":"fractured same wrist two years ago, in an injury, took two months to\
  heal","lifestyle":"plays a lot of soccer, eats well"}'
example_answer = '{"Wrist sprain/strain":{"probability":"Very High","summary":"Stretching or tearing of wrist\
  ligaments due to sudden force or excessive bending, leading to pain and limited motion."},"Wrist fracture":\
  {"probability":"Moderate","summary":"A break in the bones of the wrist, which may occur from trauma or re-injury,\
  causing pain, swelling, and difficulty moving the wrist."},"Ligament Tear":{"probability":"Moderate","summary":\
  "Damage to the ligaments in the wrist, often caused by trauma, leading to pain, instability, and compromised\
  wrist function."},"Tendonitis":{"probability":"Low","summary":"Inflammation of the tendons in the wrist,\
  typically caused by repetitive or excessive use, resulting in pain and restricted movement."},"Arthritis":\
  {"probability":"Very Low","summary":"Inflammation of the joints in the wrist, which can occur at a young age\
  as well, causing pain, stiffness, and limited range of motion."}}'
print(prompt)
print(example_info)
print(example_answer)
'''
@app.route('/query')
def query():
    user_info = request.args.get('user_info')
    message = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": example_info},
                {"role": "assistant", "content": example_answer},
                {"role": "user", "content": user_info}
          ]
      )
    output = message.get('choices')[0]
    content = output.get('message')
    response = content.get('content') #OUTPUT FROM BACK-END
    return(str(response))
if __name__ == "__main__":
    app.run()
'''
