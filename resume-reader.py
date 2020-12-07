import textract
import re
import os
from resume_classification import *
from database_functionalities import *


client=connect_db()
def convert(fname, pages=None):
	text = textract.process(fname, method='pdfminer')
	return text

def getName(resume_content):
    name=""
    for st in resume_content:
        if(st!='' and st.lower()!='resume' and st.lower()!='cv' and st.lower()!='resume/cv' and name==""):
            name = st
            break
    return name

def getEmail(resume_content):
    email = ""
    regex = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    for st in resume_content:
        words = st.split(' ')
        for word in words:
            if(re.search(regex,word)):  
                email = word
                break
    return email

def getLocation(resume_content,cities):
  location = ""
  for st in resume_content:
    words = st.split(' ')
    for word in words:
      if(word in cities):
        location = word
        break
    return location

def getPhoneNumber(resume_content):
    phone = ""
    regex = """^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$"""
    for st in resume_content:
        words = st.split(' ')
        for word in words:
            if(re.search(regex,word)):  
                phone = word
                break
    return phone

def getSkills(resume_content,skills_list):
    skills = []
    # print(resume_content)
    # print(resume_content)
    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    punctuations = '''!()|-[]{};:'"\,<>./?@$%^&_~'''
    for st in resume_content:
        no_punct = ""
        for char in st:
          if char not in punctuations:
              no_punct = no_punct + char
        words = no_punct.split(' ')
        # words = words + no_punct.split(',')
        # words = words + no_punct.split('|')
        l = no_punct.split()
        result = []
        for i in range(len(l) - 1):
            result.append(l[i] + ' ' + l[i+1])
        # print(result)
        words = list(set(list(set(words))+list(set(result))))
        # print(words)
        for word in words:
            if(word.lower().strip() in skills_list or word.strip() in skills_list):  
                skills.append(word.lower().strip())
    return list(set(skills))


def read_skills_dataset():
    df = pd.read_csv("./Datasets/new_skills.csv")
    skills_list = list(df["skills"].values)
    skills_list_lower=[]
    for i in skills_list:
        skills_list_lower.append(str(i).lower())
    return skills_list_lower



def parseSingleResume(name,skills_list,insert=1):
    folder="./CV/"+name
    resume = convert(folder).decode('utf-8')
    resume = resume.replace(u'\xa0',u'')
    resume = resume.replace(u'\u200b',u'')
    data = resume
    data = data.replace(',', ' ,')
    data = data.replace('. ', ' . ').lower()
    resume_text = data.split('\n')
    skills = list(getSkills(resume_text, skills_list))
    categories = list(getClassification(skills))
    email=getEmail(resume_text)
    phone=getPhoneNumber(resume_text)
    d = {
        "skills": skills,
        "filename": name,
        "category": categories,
        "email":email,
        "contact":phone
    }
    print(getEmail(resume_text),getPhoneNumber(resume_text))
    print(d)
    if(insert and d["contact"]!="" and d["contact"]!=""):
        insert_resume(client,d)


def get_all_file_skills_and_insert(skills_list):
    new_cvs_folder = 'CV/'
    entries = os.listdir(new_cvs_folder)
    for i in range(0,len(entries)):
        print(i)
        print("Parsing and inserting ... ",entries[i])
        try:
            parseSingleResume(entries[i],skills_list,1)
        except:
            print("error in ",entries[i])

# resume = convert('CVs/c2.pdf').decode('utf-8')

if __name__ == "__main__":
    skills_list = read_skills_dataset()
    # parseSingleResume("AshishSingh17103205 - Ashish Singh.pdf",skills_list,1)
    get_all_file_skills_and_insert(skills_list)
