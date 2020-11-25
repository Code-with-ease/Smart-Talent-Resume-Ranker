import textract
import re
import pandas as pd
import numpy as np
import unidecode
import json
import os
import shutil
from resume_classification import *
from database_functionalities import *

def convert(fname, pages=None):
	text = textract.process(fname, method='pdfminer')
	return text

def getName(resume_content):
    name=""
    for st in resume_string:
        if(st!='' and st.lower()!='resume' and st.lower()!='cv' and st.lower()!='resume/cv' and name==""):
            name = st
            break
    return name

def getEmail(resume_content):
    email = ""
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
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
    regex = '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'
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
    df = pd.read_csv("skill_set.csv")
    skills_list = list(df["skills"].values)
    skills_list_lower=[]
    for i in skills_list:
        skills_list_lower.append(str(i).lower())
    return skills_list_lower

def get_all_file_skills_and_insert(skills_list):
    json_list=[]
    new_cvs_folder = 'test_cvs/'
    resume_in_db = 'resumes_in_db/'
    entries = os.listdir(new_cvs_folder)
    for i in range(0,len(entries)):
        resume = convert(new_cvs_folder+entries[i]).decode('utf-8')
        data = resume
        data = data.replace(',',' ,')
        data = data.replace('. ',' . ')
        resume_text = data.split('\n')
        skills = list(getSkills(resume_text,skills_list))
        categories = list(get_category(skills))
        print(i,skills,categories)
        # skills = list(skills)
        d = {
            "skills":skills,
            "filename":entries[i],
            "category":categories
        }
        connect = connect_db()
        d["_id"] = str(insert_resume(connect,d))
        os.rename(new_cvs_folder+entries[i], resume_in_db+entries[i])
        json_list.append(d)
    return json_list


def parseSingleResume(name,skill_list,insert=1):
    folder="./cv/"+name
    resume = convert(folder).decode('utf-8')
    data = resume
    data = data.replace(',', ' ,')
    data = data.replace('. ', ' . ')
    resume_text = data.split('\n')
    skills = list(getSkills(resume_text, skills_list))
    categories = list(get_category(skills))
    d = {
        "skills": skills,
        "filename": name,
        "category": categories
    }
    connect = connect_db()
    print(d)

# resume = convert('CVs/c2.pdf').decode('utf-8')

if __name__ == "__main__":
    skills_list = read_skills_dataset()
    # json_list = get_all_file_skills_and_insert(skills_list)
    parseSingleResume("17103172_rishi_singhal_id_dp(1) - Rishi Singhal.pdf",skills_list,0)
    # for ob in json_list:
    #     json_string = json.dumps(ob)
    #     print(json_string)
    # print(skills)