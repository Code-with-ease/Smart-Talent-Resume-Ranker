from pymongo import MongoClient
import dns
from bson.objectid import ObjectId
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def connect_db():
  client = MongoClient()
  client = MongoClient('mongodb+srv://admin:admin@cluster0.ekv0t.mongodb.net/Resume-parser?retryWrites=true&w=majority')
  return client

def find_jd_by_details(client,details):
  db = client["Resume-parser"]
  jd_collection = db.jobs
  # ObjectId id = new ObjectId();
  # details['_id'] = ObjectId()
  jd = jd_collection.find_one(details)
  return jd


def getResumesWithCategory(category):
    db = client["Resume-parser"]
    resume_collection = db.resumes
    details = resume_collection.find({"category":category})
    return details


def getSimmilarity(resume_skills,jd_skills,vectorizer1):

    resume_arr = vectorizer1.transform([",".join(resume_skills)])

    jd_arr = vectorizer1.transform([",".join(jd_skills)])




    return cosine_similarity(resume_arr.toarray(), jd_arr.toarray())

def getMatchingResumes(jd,vectorizer1):
    resumes=getResumesWithCategory(jd["category"])
    data=[]
    for resume in resumes:
        ans=getSimmilarity(resume['skills'],jd['skills'],vectorizer1)
        data.append({"name":resume["filename"],"match":ans[0][0]})

    print(data)



client=connect_db()
jd=find_jd_by_details(client,{"company_name":"abc"})
vectorizer=CountVectorizer()
vocabulary=vectorizer.fit([",".join(jd["skills"])])
print(vocabulary)
print(vocabulary.get_feature_names())



print(jd)

getMatchingResumes(jd,vectorizer)