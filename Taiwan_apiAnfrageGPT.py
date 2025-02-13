import openai
from openai import OpenAI
import os
import dotenv
from dotenv import load_dotenv, find_dotenv
import re
import json

# Beispiel-Text, aus dem Triplets extrahiert werden sollen.
# Du kannst diesen Text ersetzen oder dynamisch befüllen.
chunk = """
        Russian forces conducted large-scale missile and drone strikes targeting Ukrainian energy infrastructure on the night of May 7 to 8, continuing to exploit Ukraine's degraded air defense umbrella ahead of the arrival of US and Western security assistance at scale. Ukrainian Air Force Commander Lieutenant General Mykola Oleshchuk reported on May 8 that Russian forces launched 21 Shahed-136/131 drones and 55 missiles, including 45 Kh-101/555 cruise missiles, four Kalibr sea-launched cruise missiles, two Iskander-M ballistic missiles, an Iskander-K ballistic missile, two Kh-59/69 cruise missiles, and a Kh-47 "Kinzhal" aeroballistic missile.[1] Oleshchuk reported that Ukrainian forces intercepted 33 Kh-101/555 cruise missiles, all four Kalibr cruise missiles, both Kh-59/69 cruise missiles, and 20 Shaheds.[2] Ukrainian Energy Minister Herman Halushchenko reported that Russian forces struck electricity generation and transmission facilities in Poltava, Kirovohrad, Zaporizhia, Lviv, Ivano-Frankivsk, and Vinnytsia oblasts.[3] Ukraine’s largest private energy operator DTEK reported that Russian forces attacked three unspecified thermal power plants (TPPs) in Ukraine and seriously damaged unspecified equipment.[4] Ukrainian state electricity transmission operator Ukrenergo spokesperson Maria Tsaturyan stated that regional energy authorities will implement shutdowns evenly across all oblasts in Ukraine due to energy shortages and warned that the Ukrenergo control center will issue a command for emergency shutdowns throughout Ukraine if consumption continues to grow in the evening.[5] Ukrainian state railway operator Ukrzaliznytsia reported that Russian forces also targeted railway infrastructure in Kherson Oblast, forcing railway administrators to reduce train travel along the Kyiv-Kherson and Kyiv-Mykolaiv routes.[6] The Russian Ministry of Defense (MoD) claimed that it targeted Ukrainian energy facilities and defense industrial enterprises in order to reduce Ukraine's ability to produce military materiel and transfer Western materiel to the frontline.[7]

        This is the fifth large scale Russian missile and drone strike targeting Ukrainian energy infrastructure since March 22, 2024, as the Russian military has attempted to exploit degraded Ukrainian air defense capabilities in spring 2024 to collapse Ukraine's energy grid and constrain Ukraine's defense industrial capacity.[8] Russian forces will likely continue to conduct mass strikes to cause long-term damage to Ukrainian energy infrastructure as degraded Ukrainian air defense capabilities persist until the arrival of US-provided air defense missiles and other Western air defense assets at scale.[9] Russian forces have also intensified strikes against Ukrainian transportation infrastructure in recent weeks in an apparent effort to disrupt Ukrainian ground lines of communication (GLOCs) and constrain the flow of expected US security assistance to the frontline.[10] Russian forces have continued to heavily target Ukrainian energy facilities in limited larger missile and drone strike series, however, suggesting that Russia is either prioritizing the effort to collapse the energy grid over interdiction efforts or must use a larger number of missiles to penetrate Ukrainian air defenses near energy facilities and cause significant damage to these facilities.

        Recent satellite imagery of depleted Russian military vehicle and weapon storage facilities further indicates that Russia is currently sustaining its war effort largely by pulling from storage rather than by manufacturing new vehicles and certain weapons at scale. Newsweek reported on May 8 that a social media source tracking Russian military depots stated that satellite imagery indicates that Russia's vehicle stores have significantly decreased from pre-war levels by nearly 32 percent from 15,152 in 2021 to 10,389 as of May 2024.[11] The military depot tracker noted that Russia has pulled most from its stores of MT-LB multipurpose armored fighting vehicles (AFVs), which are down from 2,527 prewar to 922 remaining; BMD airborne amphibious tracked infantry fighting vehicles (IFVs), which are down from 637 prewar to 244 remaining; and BTR-50 armored personnel carriers (APCs), down from 125 prewar to 52 remaining. The military depot tracker noted that it observed fewer model BTR-60s, -70s, and -80s in storage and that only 2,605 remain in storage compared with observed prewar stocks of 3,313. The military depot tracker noted that Russia is currently fielding 1,000–2,000 of its remaining MT-LBs in Ukraine. Another open-source account on X (formerly Twitter) cited satellite imagery dated May 27, 2020 and March 26, 2024 and concluded that Russia has pulled roughly 60 percent of its artillery systems at an unspecified towed artillery storage base, reportedly one of Russia's largest.[12] The source reported that about half of the remaining artillery systems at this base are likely unusable due to degradation while in storage and because many of the remaining systems are Second World War era artillery systems incompatible with modern ammunition.[13]

        Russia is relying on vast Soviet-era stores of vehicles and other equipment to sustain operations and losses in Ukraine at a level far higher than the current Russian DIB could support, nor will Russia be able to mobilize its DIB to replenish these stores for many years. The British International Institute for Strategic Studies (IISS) think tank reported on February 12 that Russia is likely able to sustain its current rate of vehicle losses (over 3,000 armored fighting vehicles annually) for at least two or three years by mainly reactivating vehicles from storage.[14] The IISS also estimated that Russia has lost over 3,000 armored fighting vehicles in 2023 and close to 8,000 armored fighting vehicles since February 2022, and that Russia likely reactivated at least 1,180 main battle tanks and about 2,470 infantry fighting vehicles and armored personnel carriers pulled from storage in 2023.[15] Ukrainian military observer Kostyantyn Mashovets reported on February 4 that the Russian defense industrial base (DIB) can produce 250–300 new and modernized tanks per year and repair an additional 250–300 tanks per year.[16] Russia will likely struggle to adequately supply its units with materiel in the long term without transferring the Russian economy to a wartime footing — a move that Russian President Vladimir Putin has sought to avoid thus far.[17]

        The Georgian State Security Service (SUS) is employing standard Kremlin information operations against Georgians protesting Georgia's Russian-style "foreign agents" bill following the lead of Georgian Dream party founder and former Georgian Prime Minister Bidzina Ivanishvili. The SUS claimed on May 8 that "certain groups of people" funded by foreign countries, party leaders, and non-governmental organizations (NGOs) are trying to organize provocations at protests against the "foreign agents" law.[18] The SUS claimed that Georgian citizens living abroad, particularly those fighting in Ukraine, are planning to conduct acts of violence against Georgian law enforcement and block and burn government buildings. The SUS further claimed that the alleged provocateurs are attempting to cause riots and chaos to cause "Maidanization" and that these methods have been used to organize "color revolutions." The SUS' references to Ukraine's Euromaidan Revolution in 2014, which drove out Ukraine's Russia-friendly president Viktor Yanukovych, and its reference to color revolutions — attempts at democratization in post-Soviet countries — mirror boilerplate Russian rhetoric attempting to blame the West for inciting and directing perceived anti-Russian protests to frame domestic dissent and calls for democratization as illegitimate.[19] The SUS made similar claims in September 2023 and alleged that former Georgian officials, Ukrainian military intelligence officials of Georgian descent, and Georgians fighting with Ukrainian forces in Ukraine were plotting a violent coup.[20] Ivanishvili recently reiterated a series of standard anti-Western and pseudohistorical Kremlin narratives during his first public speech since announcing his return to Georgian politics.[21] Ivanishvili's and the SUS' intensified use of established Kremlin information operations and increasing rhetorical alignment with Russia against the West indicate that Georgian Dream actors likely intend to purposefully derail long-term Georgian efforts for Euro-Atlantic integration, which plays into continued Russian hybrid operations to divide, destabilize, and weaken Georgia.[22]

        Armenia's efforts to distance itself from Russia are increasingly forcing the Kremlin to acknowledge issues in the bilateral relationship. Russian President Vladimir Putin and Armenian Prime Minister Nikol Pashinyan met in Moscow on May 8 following a meeting of the Eurasian Economic Union (EAEU).[23] Putin claimed that Russian-Armenian bilateral relations are "developing successfully," but noted that there are "questions" regarding security in the South Caucasus that the two will discuss privately. Pashinyan stated that "questions have accumulated that need to be discussed" since the two met in December 2023. Kremlin Spokesperson Dmitry Peskov stated that there are "problematic issues" in the bilateral relationship in response to a question about how difficult the meeting would be but claimed that both Putin and Pashinyan are willing to discuss these issues.[24] Peskov claimed that Russia is "rather optimistic" about the future of the bilateral relationship. Peskov and Putin have previously publicly attempted to downplay tension in Russian–Armenian relations, although Russian Foreign Minister Sergei Lavrov has made several frank assessments of the deteriorating relationship and issued public threats against Armenia in recent months.[25] Armenian Ministry of Foreign Affairs (MFA) Spokesperson Ani Badalyan told Radar Armenia on May 7 that Armenia will not contribute to the Russian-led Collective Security Treaty Organization's (CSTO) budget in 2024.[26] An unnamed source within the CSTO told Kremlin newswire TASS that the CSTO is aware of Armenia's decision but noted that Armenia remains a member of the CSTO.[27] Armenia's decision to stop financing CSTO activities is the latest in a series of decisions to pivot away from Russian-led political and security organizations, including continuing to make Armenia's involvement in the CSTO increasingly nominal, over the past eight months.[28]

        Lithuanian Prime Minister Ingrida Šimonytė stated that the Lithuanian government has granted permission for Lithuania to send troops to Ukraine for training missions in the future.[29] Šimonytė stated during an interview with the Financial Times (FT) published on May 8 that Ukraine has not requested Lithuanian troops and noted that Russia would likely see the deployment of Lithuanian troops to Ukraine as a provocation. Šimonytė stated that if Europe only considered Russia's response to manpower and materiel assistance to Ukraine, Europe would not send anything and stated that "every second week you hear that somebody will be nuked [by Russia]." French President Emmanuel Macron called on Europe to build a strategic concept of "credible European defense" during a speech on April 25 and has previously urged the West to not "rule out" the possibility of sending Western troops to Ukraine in the future.[30]

        Reports indicate that there is an available open-source tool that allows people to search by specific coordinates for Telegram users who have enabled a certain location-sharing setting. Russian opposition outlet Meduza reported on May 8 that this tool allows people to input coordinates to discover all Telegram users who have enabled the "find people nearby" setting located within 50–100 meters of the coordinates.[31] Meduza noted that the "find people nearby" setting usually only allows users to find other Telegram users within 50–100 meters of their current location. Users can enable or disable this location-sharing setting in the "contacts" settings of the application.

        Key Takeaways:

        Russian forces conducted large-scale missile and drone strikes targeting Ukrainian energy infrastructure on the night of May 7 to 8, continuing to exploit Ukraines degraded air defense umbrella ahead of the arrival of US and Western security assistance at scale.
        Recent satellite imagery of depleted Russian military vehicle and weapons storage facilities further indicates that Russia is currently sustaining its war effort largely by pulling from storage rather than by manufacturing new vehicles and certain weapons at scale.
        Russia is relying on vast Soviet-era stores of vehicles and other equipment to sustain operations and losses in Ukraine at a level far higher than the current Russian DIB could support, nor will Russia be able to mobilize its DIB to replenish these stores for many years.
        The Georgian State Security Service (SUS) is employing standard Kremlin information operations against Georgians protesting Georgia's Russian-style "foreign agents" bill following the lead of Georgian Dream party founder and former Georgian Prime Minister Bidzina Ivanishvili.
        Armenia's efforts to distance itself from Russia are increasingly forcing the Kremlin to acknowledge issues in the bilateral relationship.
        Lithuanian Prime Minister Ingrida Šimonytė stated that the Lithuanian government has granted permission for Lithuania to send troops to Ukraine for training missions in the future.
        Reports indicate that there is an available open-source tool that allows people to search by specific coordinates for Telegram users who have enabled a certain location-sharing setting.
        Russian forces recently advanced near Svatove, Kreminna, and Avdiivka and in the Donetsk-Zaporizhia Oblast border area.
        Russian Defense Minister Sergei Shoigu continues to highlight Russian formations involved in Russia’s invasion of Ukraine.
        """

# Lade Umgebungsvariablen (z.B. OPENAI_API_KEY) aus einer .env
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def get_completion(prompt, model='gpt-3.5-turbo'):
    """
    Sendet einen Prompt an das OpenAI-API und gibt das Completion-Resultat zurück.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=500,
    )
    return completion.choices[0].message.content

def generate_cypher_queries():
    """
    1) Erstellt einen Prompt, um aus dem Text in 'chunk' Triplets zu extrahieren.
    2) Fragt GPT, um Triplets in folgendem Format zu bekommen:
       <triplet><subj>...</subj><obj>...</obj><rel>...</rel></triplet>
    3) Wandelt jedes Triplet in genau ein Cypher-Statement um.
    4) Gibt die Liste (Array) aller generierten Statements zurück.
    """
    prompt = f"""
    Analyze the following text and extract all relevant relationships, 
    formatting them as triplets:

    <triplet><subj>Subject</subj><obj>Object</obj><rel>Relationship</rel></triplet>

    Text: {chunk}

    Guidelines:
    1. Identify at least 3 distinct, relevant relationships per chunk (1 sentence).
    2. Focus on geopolitical, economic, and diplomatic connections.
    3. Relationships should be clear, concise, and factual.
    4. Include relationships between countries, political figures, organizations, and key concepts.
    5. Use simple, direct phrases for relationships (e.g., "is president of", "shares border with", "opposes", "supports").
    6. Avoid overly verbose or complex relationship descriptions.
    7. Ensure each triplet represents a complete, standalone fact.

    Examples of relationship types to look for:
    - Political leadership
    - Geographical
    - Economic ties
    - Diplomatic stances
    - Military alliances
    - Historical context

    Extract all relevant relationships from the text, prioritizing accuracy and relevance 
    to the text's main themes.
    """
    # 1) Hole die Triplets von GPT
    triplets = get_completion(prompt)
    # 2) Erstelle daraus Cypher-Queries
    return generate_cypher_from_triplets(triplets)

def generate_cypher_from_triplets(triplets):
    """
    Parst die Triplets via Regex aus dem GPT-Resultat und 
    baut für jedes Triplet ein einzelnes Cypher-Query-Statement.
    """
    # Alle Triplets im Format:
    # <triplet><subj>...</subj><obj>...</obj><rel>...</rel></triplet>
    triplet_pattern = r"<triplet><subj>(.*?)</subj><obj>(.*?)</obj><rel>(.*?)</rel></triplet>"
    matches = re.findall(triplet_pattern, triplets)

    cypher_queries = []
    for subj, obj, rel in matches:
        # 1) Relationship und Knoten-Namen robust "säubern".
        #    - z.B. alle Sonderzeichen in '_' umwandeln.
        #    - Relationship TYP darf keine Minus- oder Sonderzeichen enthalten.
        rel_sanitized = sanitize_for_cypher_rel(rel)
        subj_sanitized = sanitize_for_cypher_node(subj)
        obj_sanitized  = sanitize_for_cypher_node(obj)

        # 2) JSON-escape der fertigen Knoten-Namen, 
        #    damit Apostrophe, Anführungszeichen usw. keine Fehler mehr werfen.
        subj_escaped = json.dumps(subj_sanitized)
        obj_escaped  = json.dumps(obj_sanitized)

        # 3) Baue das einzelne Cypher-Query
        cypher_query = f"""
            MERGE (a:Person {{name: {subj_escaped}}})
            MERGE (b:Person {{name: {obj_escaped}}})
            MERGE (a)-[:{rel_sanitized}]->(b)
        """
        # Leerzeilen entfernen
        cypher_queries.append(cypher_query.strip())

    return cypher_queries

def sanitize_for_cypher_rel(input_string):
    """
    Entfernt alle Zeichen außer Buchstaben, Ziffern und '_' und 
    wandelt den restlichen String in GROSSBUCHSTABEN um.
    -> Geeignet für Relationship Types.
    """
    # Ersetze alles, was nicht a-z/A-Z/0-9/_ ist, durch '_'
    out = re.sub(r'[^A-Za-z0-9_]+', '_', input_string)
    return out.upper()

def sanitize_for_cypher_node(input_string):
    """
    Für Knoten-Namen kann man grundsätzlich dieselbe Methode verwenden,
    z.B. auf Lowercase oder gemischtes Case. 
    Hier ersetzen wir nur "harte" Sonderzeichen durch '_',
    um Syntax-Fehler zu vermeiden, behalten Buchstaben und Ziffern.
    """
    # Beispiel: Konvertiere alle nicht erlaubten Zeichen in '_'
    # -> hier bleiben Buchstaben, Ziffern und Unterstriche erlaubt
    out = re.sub(r'[^A-Za-z0-9_]+', '_', input_string)
    # optional: out = out.lower() / je nach Geschmack
    return out

if __name__ == "__main__":
    # Kleiner Test, wenn die Datei direkt ausgeführt wird:
    result_queries = generate_cypher_queries()
    print("**Generated Cypher Queries**")
    for q in result_queries:
        print(q)
