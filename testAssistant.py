from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
from flask import Flask, request, jsonify
import json


# import and define OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(
    api_key=OPENAI_KEY,
)
ASSISTANT_KEY = os.getenv("ASSISTANT_KEY")
meet_or_not_asst = ASSISTANT_KEY

## import user inputs for meeting info && parse into message/file
with open('sample_input.json', 'r') as file:
    data = json.load(file)
# Extract user inputs from the request
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
thread = client.beta.threads.create(
)
# get thread id
thread_id = thread.id

# Create the user message and add it to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=message,
)

# create run
run = client.beta.threads.runs.create(
    thread_id = thread_id,
    assistant_id=meet_or_not_asst
)
# get run id
run_id = run.id

while run.status != "completed":
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")
    
    if keep_retrieving_run.status == "completed":
        print("\n")
        break

# Retrieve messages added by the Assistant to the thread
all_messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

# Print the messages from the user and the assistant
print("###################################################### \n")
print(f"USER: {message.content[0].text.value}")
print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")


# Extract and structure the API response into a meeting agenda format
