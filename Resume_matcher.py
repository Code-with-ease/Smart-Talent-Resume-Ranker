from pymongo import MongoClient
import dns
from bson.objectid import ObjectId
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def connect_db():
  client = MongoClient('mongodb+srv://admin:admin@cluster0.ekv0t.mongodb.net/Resume-parser?retryWrites=true&w=majority')
  return client

client=connect_db()


def getScore(resume_arr,jd_arr):
    score=0
    for idx in range(0,len(resume_arr)):
        if(resume_arr[idx]==jd_arr[idx]):
            score=score+1
    return (score/len(jd_arr))

def find_jd_by_details(client,details):
  db = client["Resume-parser"]
  jd_collection = db.jobs
  jd = jd_collection.find_one(details)
  return jd


def getResumesWithCategory(category):
    db = client["Resume-parser"]
    resume_collection = db.resumes
    details = resume_collection.find({"category":category})
    return details


def getSimmilarity(resume_skills,jd_skills,vectorizer1):
    resume_arr = vectorizer1.transform([" ".join(resume_skills)])
    jd_arr = vectorizer1.transform([" ".join(jd_skills)])
    print(resume_arr.toarray(),jd_arr.toarray())
    return getScore(resume_arr.toarray()[0], jd_arr.toarray()[0])


def getMatchingResumes(jd,vectorizer1):
    resumes=getResumesWithCategory(jd["category"])
    data=[]
    for resume in resumes:
        ans=getSimmilarity(resume['skills'],jd['skills'],vectorizer1)
        data.append({"name":resume["filename"],"match":ans})
    print(data)


def getResumeRanking(jd_name):
    client=connect_db()
    jd=find_jd_by_details(client,{"filename":jd_name})
    vectorizer=CountVectorizer(tokenizer=lambda txt: txt.split())
    vocabulary=vectorizer.fit([" ".join(jd["skills"])])
    print(vocabulary.get_feature_names())
    getMatchingResumes(jd,vectorizer)



getResumeRanking("jd01.pdf")
