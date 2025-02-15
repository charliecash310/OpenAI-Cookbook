import openai
import os
from mitreattack.stix20 import MitreAttackData

# ASCII Art Title
ascii_art = """

                                                                                                                  
                                                      ,;                                                    ., G:      
                       t           j.               f#i                                                    ,Wt E#,    :
            ..       : Ej GEEEEEEELEW,            .E#t                    .. GEEEEEEEL GEEEEEEEL          i#D. E#t  .GE
           ,W,     .Et E#,,;;L#K;;.E##j          i#W,                    ;W, ,;;L#K;;. ,;;L#K;;.         f#f   E#t j#K;
          t##,    ,W#t E#t   t#E   E###D.       L#D.                    j##,    t#E       t#E          .D#i    E#GK#f  
         L###,   j###t E#t   t#E   E#jG#W;    :K#Wfff;                 G###,    t#E       t#E         :KW,     E##D.   
       .E#j##,  G#fE#t E#t   t#E   E#t t##f   i##WLLLLt              :E####,    t#E       t#E         t#f      E##Wi   
      ;WW; ##,:K#i E#t E#t   t#E   E#t  :K#E:  .E#L                 ;W#DG##,    t#E       t#E   ___    ;#G     E#jL#D: 
     j#E.  ##f#W,  E#t E#t   t#E   E#KDDDD###i   f#E:              j###DW##,    t#E       t#E  ( _ )    :KE.   E#t ,K#j
   .D#L    ###K:   E#t E#t   t#E   E#f,t#Wi,,,    ,WW;            G##i,,G##,    t#E       t#E  / _ \/\   .DW:  E#t   jD
  :K#t     ##D.    E#t E#t   t#E   E#t  ;#W:       .D#;         :K#K:   L##,    t#E       t#E | (_>  <     L#, j#t     
  ...      #G      ..  E#t    fE   DWi   ,KK:        tt        ;##D.    L##,     fE        fE  \___/\/      jt  ,;     
           j           ,;.     :                               ,,,      .,,       :         :                          
                                                                                                                       
                                                                                                  
"""

print(ascii_art)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the MITRE ATT&CK dataset
mitre_attack_data = MitreAttackData("/home/kali/Desktop/SORT/OpenAI/Chapter 6/cti/enterprise-attack/enterprise-attack.json")

# Function to extract keywords from the given description
def extract_keywords_from_description(description):
    prompt = (
        f"Given the cybersecurity scenario description: '{description}', "
        "identify and list the key terms, techniques, or technologies relevant to MITRE ATT&CK. "
        "Extract TTPs from the scenario. If the description is too basic, expand upon it with "
        "additional details, applicable campaign, or attack types based on dataset knowledge. "
        "Then, extract the TTPs from the revised description."
    )

    messages = [
        {"role": "system", "content": "You are a cybersecurity professional with more than 25 years of experience."},
        {"role": "user", "content": prompt},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
        )
        response_content = response.choices[0].message.content.strip()
        keywords = response_content.split(', ')
        return keywords
    except Exception as e:
        print("An error occurred while connecting to the OpenAI API:", e)
        return []

# Function to score matches based on keywords
def score_matches(matches, keywords):
    scores = []
    for match in matches:
        score = (
            sum([keyword in match['name'] for keyword in keywords]) +
            sum([keyword in match.get('description', '') for keyword in keywords])
        )
        scores.append((match, score))
    return scores

# Function to search the MITRE ATT&CK dataset for matches
def search_dataset_for_matches(keywords):
    matches = []
    for item in mitre_attack_data.get_techniques():
        if any(keyword in item['name'] for keyword in keywords) or \
           any(keyword in item.get('description', '') for keyword in keywords):
            matches.append(item)
    return matches

# Function to generate a TTP chain for a match
def generate_ttp_chain(match):
    prompt = (
        f"Given the MITRE ATT&CK technique '{match['name']}' and its description '{match['description']}', "
        "generate an example scenario and TTP chain demonstrating its use."
    )

    messages = [
        {"role": "system", "content": "You are a cybersecurity professional with expertise in MITRE ATT&CK techniques."},
        {"role": "user", "content": prompt},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
        )
        response_content = response.choices[0].message.content.strip()
        return response_content
    except Exception as e:
        print("An error occurred while generating the TTP chain:", e)
        return "Unable to generate TTP chain."

# Main execution
if __name__ == "__main__":
    description = input("Enter your scenario description: ")
    keywords = extract_keywords_from_description(description)
    matches = search_dataset_for_matches(keywords)
    scored_matches = score_matches(matches, keywords)
    top_matches = sorted(scored_matches, key=lambda x: x[1], reverse=True)[:3]

    print("\nTop 3 matches from the MITRE ATT&CK dataset:")
    for match, score in top_matches:
        print(f"Name: {match['name']}")
        print(f"Summary: {match.get('description', 'No description available.')}")
        ttp_chain = generate_ttp_chain(match)
        print(f"Example Scenario and TTP Chain: {ttp_chain}")
        print("-" * 50)
