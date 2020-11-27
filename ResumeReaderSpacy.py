import spacy
import pandas as pd
from spacy.lang.en import English


def convertToLower(skills):
    lower=[]
    for skill in skills:
        if(skill==skill):
            lower.append(skill.lower())
    return lower

nlp=English()
data=pd.read_csv("skill_set.csv")

skills_from_csv=data["skills"].values
skills_lower=convertToLower(skills_from_csv)
doc=nlp(",".join(skills_lower))

token_list = []
for token in doc:
    token_list.append(token.text)
print(token_list)



