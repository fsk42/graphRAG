import openai
from openai import OpenAI
import os
import dotenv
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def get_completion(prompt, model='gpt-3.5-turbo'):
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=250,
    )
    return completion.choices[0].message.content

# Create a prompt for generating Cypher queries for node creation
def generate_cypher_queries():
    prompt = """
    extract the most significant keywords from the question below. 
    For each keyword also return different conjugations of the word. 
    Return them as a list of plain keywords simply separated by a comma. 

    What has happened to Ukrainian energy facilities?
    """
    return get_completion(prompt)

# Example usage: Generate Cypher queries
cypher_queries = generate_cypher_queries()
print(cypher_queries)
