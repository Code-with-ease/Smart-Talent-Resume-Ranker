import textract
import re
import sys
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

def convert(fname):
    try:
	    text = textract.process(fname, method='pdfminer')
	    return text
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def connect_db():
    try:
        client = MongoClient('mongodb+srv://admin:admin@cluster0.ekv0t.mongodb.net/Resume-parser?retryWrites=true&w=majority')
        return client
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def insert_jd(client,details):
    try:
        db = client["Resume-parser"]
        jd_collection = db.jobs
        details['_id'] = ObjectId()
        resume_id = jd_collection.insert_one(details).inserted_id
        return resume_id
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise




def getSkills(resume_content,skills_list):
    try:
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
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return []
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def read_skills_dataset():
    try:
        df = pd.read_csv("./Datasets/new_skills.csv")
        skills_list = list(df["skills"].values)
        skills_list_lower=[]
        for i in skills_list:
            skills_list_lower.append(str(i).lower())
        return skills_list_lower
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return []
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return []


def getCompanyName(jd_arr):
    try:
        ans=""
        for elem in jd_arr:
            print(elem)
            arr=elem.split(":")
            if(len(arr) and arr[0].strip().lower()=="company name"):
                ans= arr[1].strip()
                break
        return ans
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return ""
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return ""


def getCategory(jd_arr):
    try:
        ans=""
        for elem in jd_arr:
            arr = elem.split(":")
            if (len(arr) and arr[0].strip().lower() == "category"):
                for i in range(1,len(arr)):
                    ans=ans+arr[i]+" "
        return ans
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return ""
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return ""


def getDescription(jd_arr):
    try:
        ans=""
        for elem in jd_arr:
            arr = elem.split(":")
            if (len(arr) and arr[0].strip().lower() == "description"):
                for i in range(1,len(arr)):
                    ans=ans+arr[i].strip()+" "
                break
        return ans
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return ""
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return ""



def getInfo(jd_arr):
    try:
        data={}
        data["company_name"]=getCompanyName(jd_arr)
        data["category"] = getCategory(jd_arr)
        description = getDescription(jd_arr)
        skills_list = read_skills_dataset()
        description=description.split("\n")
        print("Description : ",description)
        skills_list = getSkills(description,skills_list)
        data["skills"]=skills_list
        return data
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return {}
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return {}

def insertJdIntoDb(data):
    try:
        connect = connect_db()
        insert_jd(connect,data)
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def parseJd(filename,insert=1):
    try:
        text = convert("./JD/"+filename).decode('utf-8')
        jd_arr = re.split(r'[\n\r]{2,}', text)
        data=getInfo(jd_arr)
        data["filename"]=filename
        print(data)
        if(insert):
            insertJdIntoDb(data)
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

parseJd("jd02.pdf",0)




