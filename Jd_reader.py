import textract
import re

import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

def convert(fname):
	text = textract.process(fname, method='pdfminer')
	return text

def connect_db():
  client = MongoClient('mongodb+srv://admin:admin@cluster0.ekv0t.mongodb.net/Resume-parser?retryWrites=true&w=majority')
  return client

def insert_jd(client,details):
  db = client["Resume-parser"]
  jd_collection = db.jobs
  details['_id'] = ObjectId()
  resume_id = jd_collection.insert_one(details).inserted_id
  return resume_id


def getSkills(resume_content,skills_list):
    skills = []
    punctuations = '''!()|-[]{};:'"\,<>./?@$%^&_~'''
    for st in resume_content:
        no_punct = ""
        for char in st:
          if char not in punctuations:
              no_punct = no_punct + char
        words = no_punct.split(' ')
        l = no_punct.split()
        result = []
        for i in range(len(l) - 1):
            result.append(l[i] + ' ' + l[i+1])
        words = list(set(list(set(words))+list(set(result))))
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


def getCompanyName(jd_arr):
    ans=""
    for elem in jd_arr:
        print(elem)
        arr=elem.split(":")
        if(len(arr) and arr[0].strip().lower()=="company name"):
            ans= arr[1].strip()
            break

    return ans


def getCategory(jd_arr):
    ans=""
    for elem in jd_arr:
        arr = elem.split(":")
        if (len(arr) and arr[0].strip().lower() == "category"):
            return arr[1].strip()
            break
    return ans


def getDescription(jd_arr):
    ans=""
    for elem in jd_arr:
        arr = elem.split(":")
        if (len(arr) and arr[0].strip().lower() == "description"):
            ans= arr[1].strip()
            break
    return ans



def getInfo(jd_arr):
    data={}
    data["company_name"]=getCompanyName(jd_arr)
    data["category"] = getCategory(jd_arr)
    description = getDescription(jd_arr)
    print(description)
    skills_list = read_skills_dataset()
    skills_list = getSkills(description.split(" "),skills_list)
    data["skills"]=skills_list
    return data

def insertJdIntoDb(data):
    connect = connect_db()
    insert_jd(connect,data)


def parseJd(filename,insert=1):
    text = convert("./JD/"+filename).decode('utf-8')
    jd_arr = re.split(r'[\n\r]{2,}', text)
    data=getInfo(jd_arr)
    data["filename"]=filename
    print(data)
    if(insert):
        insertJdIntoDb(data)

parseJd("jd01.pdf",1)







