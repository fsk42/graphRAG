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
    Answer the following question:

Question: What has happened to Ukrainian energy facilities?

Relations from the Knowledge Graph:
Russian_forces --[:TARGETING]--> Ukrainian_energy_infrastructure
Russian_forces --[:EXPLOITING]--> Ukrainian_air_defense_umbrella
Ukrainian_Air_Force_Commander_Lieutenant_General_Mykola_Oleshchuk --[:REPORTED_THAT]--> Russian_forces
Ukrainian_Air_Force_Commander_Lieutenant_General_Mykola_Oleshchuk --[:REPORTED_INTERCEPTING_MISSILES_AND_DRONES]--> Russian_forces
Russian_Ministry_of_Defense_(MoD) --[:TARGETED]--> Ukrainian_energy_facilities_and_defense_industrial_enterprises
Russian_military --[:EXPLOITING]--> Ukrainian_air_defense_capabilities
Russian_military --[:ATTEMPTED_TO_EXPLOIT]--> Ukrainian_air_defense_capabilities
Russian_forces --[:TARGETING]--> Ukrainian_transportation_infrastructure
Russian_forces --[:TARGETED]--> Ukrainian_transportation_infrastructure
Russian_forces --[:TARGETING]--> Ukrainian_energy_facilities
Russian_forces --[:HEAVILY_TARGETED]--> Ukrainian_energy_facilities
Russia --[:USING_A_LARGER_NUMBER_OF_MISSILES]--> Ukrainian_air_defenses
Russia --[:TARGETING]--> Ukraine
Russia --[:EXPLOITING]--> Ukraine
Russia --[:ATTEMPTED_TO_COLLAPSE_ENERGY_GRID]--> Ukraine
Russia --[:INTENSIFIED_STRIKES_AGAINST_TRANSPORTATION_INFRASTRUCTURE]--> Ukraine
Russia --[:HEAVILY_TARGETED_ENERGY_FACILITIES]--> Ukraine
Russia --[:ATTEMPTING_TO_COLLAPSE_ENERGY_GRID]--> Ukraine
Russia --[:INTENSIFYING_STRIKES_AGAINST_TRANSPORTATION_INFRASTRUCTURE]--> Ukraine
US_and_Western_security_assistance --[:ARRIVING_AT_SCALE]--> Ukraine
Russian_Ministry_of_Defense --[:TARGETING_ENERGY_FACILITIES_AND_DEFENSE_INDUSTRIAL_ENTERPRISES]--> Ukraine
Russia --[:CONDUCTING_MASS_STRIKES]--> Ukraine
Russia --[:COLLAPSING_ENERGY_GRID]--> Ukraine
Russia --[:CONSTRAINING_DEFENSE_INDUSTRIAL_CAPACITY]--> Ukraine
Russia --[:RELYING_ON_SOVIET_ERA_STORES_OF_VEHICLES_AND_EQUIPMENT]--> Ukraine
Russia --[:SUSTAINING_OPERATIONS_AND_LOSSES_IN_UKRAINE]--> Ukraine
Russia --[:UNABLE_TO_MOBILIZE_DEFENSE_INDUSTRIAL_BASE_TO_REPLENISH_STORES]--> Ukraine
Russia --[:PENETRATING]--> Ukraine
Russian_Ministry_of_Defense_MoD_ --[:TARGETED]--> Ukraine_s_ability_to_produce_military_materiel
Russia --[:ATTEMPTING_TO_COLLAPSE]--> Ukraine_s_energy_grid
Russia --[:COLLAPSING]--> Ukraine_s_energy_grid
Russia --[:CONSTRAINING]--> Ukraine_s_defense_industrial_capacity
Russia --[:HEAVILY]--> Ukraine_s_energy_infrastructure
Russia --[:CAUSING_SIGNIFICANT_DAMAGE_TO]--> Ukraine_s_energy_facilities
Russian_forces --[:TARGETING]--> Ukrainian_energy_infrastructure
Russian_Ministry_of_Defense_(MoD) --[:TARGETED]--> Ukrainian_energy_facilities_and_defense_industrial_enterprises
Russian_forces --[:TARGETING]--> Ukrainian_energy_facilities
Russian_forces --[:HEAVILY_TARGETED]--> Ukrainian_energy_facilities
Russia --[:ATTEMPTING_TO_COLLAPSE]--> Ukraine_s_energy_grid
Russia --[:COLLAPSING]--> Ukraine_s_energy_grid
Russia --[:HEAVILY]--> Ukraine_s_energy_infrastructure
Russia --[:CAUSING_SIGNIFICANT_DAMAGE_TO]--> Ukraine_s_energy_facilities
Russian_Ministry_of_Defense_(MoD) --[:TARGETED]--> Ukrainian_energy_facilities_and_defense_industrial_enterprises
Russian_forces --[:TARGETING]--> Ukrainian_energy_facilities
Russian_forces --[:HEAVILY_TARGETED]--> Ukrainian_energy_facilities
Russia --[:CAUSING_SIGNIFICANT_DAMAGE_TO]--> Ukraine_s_energy_facilities

Provide a clear and concise answer.
    """
    return get_completion(prompt)

# Example usage: Generate Cypher queries
cypher_queries = generate_cypher_queries()
print(cypher_queries)
