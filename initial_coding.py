import openai
import pandas as pd
from pandas import json_normalize

k=API_KEY


openai.api_key = k

def get_completion_2(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
        #n=2,
    )
    return response.choices[0].message["content"]


path = PATH
df = pd.read_csv(path+'0_chunk_data.csv', encoding ='latin-1')


#iterate over evry chunk of data
l = len(df.index)

for i in range(l):
    text = df.loc[i]['Interview_chunk']
    print (i)

    prompt = f"""
   
    An challenge is an obstacle that a person tries to overcome, in particular in relatio to accessing data and knowledge.

    Identify up tp 2 relevant challenges for the interviewee in the text below, provide a name for each challenge, 
    a summary description of the challenge and a quote from the respondent for each interest no longer than 4 lines


    Format the response as a json file keeping names, descriptions and quotes togeter in the json, and keep them
    together in 'Challenges'. 
 

     
    ```{text}```
    """

    response = get_completion_2(prompt)
    print(response)
   
#transform the json into df 
    codes= eval(response)
    df2 = json_normalize(codes['Challenges']) 
    

#this is the file where the initial list of codes reside
   
    
    
    myFile = path+'1_challenges_list.csv'
    
    df2.to_csv(myFile, header=None, mode='a')