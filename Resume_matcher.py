from pymongo import MongoClient
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from operator import itemgetter
import tabulate
import sys

def connect_db():
    try:
        client = MongoClient('mongodb+srv://admin:admin@cluster0.ekv0t.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        return client
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

client=connect_db()


import numpy as np


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(0,size_x):
        matrix [x, 0] = x
    for y in range(0,size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def getLowerDatasetCategory():
    try:
        data=pd.read_csv("./Datasets/category.csv")
        return data["category"].tolist().lower()
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return []
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return []

def getLevenstien(category,word):
    try:
        word=word.lower().replace(" ","")
        min=9999999
        word_min_dist=""
        for cat in category:

            dist=levenshtein(cat["lowerCategory"],word)
            if(dist<min):
                min=dist
                word_min_dist=cat["category"]

        return word_min_dist
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return ""
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return ""



def getScore(resume_arr,jd_arr):
    score=0
    for idx in range(0,len(resume_arr)):
        if(resume_arr[idx]==jd_arr[idx]):
            score=score+1
    return (score/len(jd_arr))

def find_jd_by_details(client,details):
   try:
       db = client["Resume-parser"]
       jd_collection = db.jobs
       jd = jd_collection.find_one(details)
       return jd
   except ValueError:
       print("Value Error :", sys.exc_info()[0])
       return []
   except:
       print("Unexpected error:", sys.exc_info()[0])
       return []



def getResumesWithCategory(category):
    try:
        db = client["Resume-parser"]
        resume_collection = db.resumes
        details = resume_collection.find({"category":category})
        return details
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return []
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return []


def getSimmilarity(resume_skills,jd_skills,vectorizer1):
    try:
        resume_arr = vectorizer1.transform([" ".join(resume_skills)])
        jd_arr = vectorizer1.transform([" ".join(jd_skills)])
        # print(resume_arr.toarray(),jd_arr.toarray())
        return getScore(resume_arr.toarray()[0], jd_arr.toarray()[0])*100
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return 0
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def getTotalCategoryCleaned():
    try:
        data = pd.read_csv("./Datasets/category.csv")
        category = data["category"].tolist()
        cat = []

        for i in category:
            temp=i.replace("Jobs","Profile")
            i = i.replace(" ", "").lower().replace("jobs", "profile")
            cat.append({"category":temp,"lowerCategory":i})

        return cat
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return []
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return []


def printScoreBoard(resumes):
    try:
        if(len(resumes)):
            header = resumes[0].keys()
            rows = [x.values() for x in resumes]
            print(tabulate.tabulate(rows, header, tablefmt='grid'))
        else:
            print("NO Resume found")
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def getMatchingResumes(jd,vectorizer1,thresh=30):
    try:
        categories = getTotalCategoryCleaned()
        levenshtein_category=getLevenstien(categories,jd["category"])
        # print(jd["category"],levenshtein_category)
        resumes=getResumesWithCategory(levenshtein_category)
        data=[]
        for resume in resumes:
            ans=getSimmilarity(resume['skills'],jd['skills'],vectorizer1)
            if(ans>=thresh and (resume['email']!="" or resume['contact']!="")):
                data.append({"name":resume["filename"],"email":resume["email"],"contact":resume["contact"],"match":ans})
        sortedReumes = sorted(data, key=itemgetter('match'), reverse=True)
        printScoreBoard(sortedReumes)
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def getResumeRanking(jd_name):
    try:
        client=connect_db()
        jd=find_jd_by_details(client,{"filename":jd_name})
        vectorizer=CountVectorizer(tokenizer=lambda txt: txt.split())
        vocabulary=vectorizer.fit([" ".join(jd["skills"])])
        # print(vocabulary.get_feature_names())
        getMatchingResumes(jd,vectorizer)
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    getResumeRanking("jd05.pdf")






