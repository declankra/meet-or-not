from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI

# import and define OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(
    api_key=OPENAI_KEY,
)
ASSISTANT_KEY = os.getenv("ASSISTANT_KEY")
meet_or_not_asst = client.beta.assistants.retrieve(ASSISTANT_KEY)

## import user inputs for meeting info && parse into message/file

## create thread
new_thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Crate a meeting agenda based off the following user's purpose, expected outcome type, expected outcome, and priority.",
      ##"file_ids": [file_id]
    }
  ]
)
thread_id = new_thread.id

# create run
run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=meet_or_not_asst
)
run_id = run.id

# check run status
run = client.beta.threads.runs.retrieve(
  thread_id=thread_id,
  run_id=run_id
)

#print thread message
thread_messages = client.beta.threads.messages.list(thread_id)
print(thread_messages.data)


