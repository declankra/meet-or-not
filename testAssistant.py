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
my_assistant = client.beta.assistants.retrieve(ASSISTANT_KEY)
