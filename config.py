# todo: Add your api key here
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv('.env')
import os




client = OpenAI(
    # This is the default and can be omitted
    api_key= os.getenv('API_KEY')
)

response  = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "write 5 animal ",
        }
    ],
    model="gpt-3.5-turbo",
    stream=False
)

print(response)