import openai
from openai import OpenAI
import os
import textwrap

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')
client = OpenAI()
def get_completion(prompt, model='gpt-3.5-turbo'):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=250,
        )
    return completion.choices[0].message.content
# print with limited width

def printw(text, width=80):
    print('\n'.join(textwrap.wrap(text, width)))
prompt = '''
Es sind drei Autos auf dem Parkplatz.
Zwei Fahrzeuge verlassen den Parklplatz,
drei Fahrzeuge kommen auf den Parkplatz.
Wie viele Autos stehen auf dem Parkplatz?
'''

printw(get_completion(prompt, model='gpt-3.5-turbo'))
#printw(get_completion(prompt, model='gpt-4o'))