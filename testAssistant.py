from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
from flask import Flask, request, jsonify


# import and define OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(
    api_key=OPENAI_KEY,
)
ASSISTANT_KEY = os.getenv("ASSISTANT_KEY")
meet_or_not_asst = client.beta.assistants.retrieve(ASSISTANT_KEY)

## import user inputs for meeting info && parse into message/file
# Extract user inputs from the request
data = request.get_json(file)
meeting_purpose = data.get('meeting_purpose')
outcome_type = data.get('expected_outcome_type')
expected_outcome = data.get('expected_outcome')
priority = data.get('priority')

# Formulate the message for the Assistant
message = (f"Based on the following user inputs, create a meeting agenda:\n"
               f"Meeting Purpose: {meeting_purpose}\n"
               f"Expected Outcome Type: {outcome_type}\n"
               f"Expected Outcome: {expected_outcome}\n"
               f"Priority: {priority}\n\n"
               )

## create thread
new_thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": message,
      ##"file_ids": [file_id]
    }
  ]
)
# get thread id
my_thread_id = new_thread.id

# create run
new_run = client.beta.threads.runs.create(
    my_thread_id = my_thread_id,
    assistant_id=meet_or_not_asst
)
# get run id
run_id = new_run.id


# print messages in thread
messages = client.beta.threads.messages.list(my_thread_id)
print(messages.data)


## print messages in thread
messages = client.beta.threads.messages.list(my_thread_id)
response = messages.data[0].content[0].text.value
response



 # Extract and structure the API response into a meeting agenda format
agenda = response.choices[0].message['content'].strip()
# Return the generated meeting agenda
jsonify({"agenda": agenda})




## check run status
##run = client.beta.threads.runs.retrieve(
 ## thread_id=thread_id,
 ##run_id=run_id
##) 