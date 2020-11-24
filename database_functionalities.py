from pymongo import MongoClient
import dns
from bson.objectid import ObjectId

def connect_db():
  client = MongoClient()
  client = MongoClient('mongodb+srv://admin:admin@cluster0.ekv0t.mongodb.net/Resume-parser?retryWrites=true&w=majority')
  return client

def insert_resume(client,details):
  db = client["Resume-parser"]
  resume_collection = db.resumes
  # ObjectId id = new ObjectId();
  details['_id'] = ObjectId()
  resume_id = resume_collection.insert_one(details).inserted_id
  return resume_id

def insert_jd(client,details):
  db = client["Resume-parser"]
  jd_collection = db.jobs
  # ObjectId id = new ObjectId();
  details['_id'] = ObjectId()
  jd_id = jd_collection.insert_one(details).inserted_id
  return jd_id

def find_jd_by_details(client,details):
  db = client["Resume-parser"]
  jd_collection = db.jobs
  # ObjectId id = new ObjectId();
  # details['_id'] = ObjectId()
  jd = jd_collection.find_one(details)
  return jd

def find_jds_by_details(client,details):
  db = client["Resume-parser"]
  jd_collection = db.jobs
  # ObjectId id = new ObjectId();
  # details['_id'] = ObjectId()
  jds = jd_collection.find(details)
  return jds

def find_resume_by_details(client,details):
  db = client["Resume-parser"]
  resume_collection = db.resumes
  details = resume_collection.find_one(details)
  return details

def find_resumes_by_skill(client,required_skill=[],one_of_skill=[]):
  db = client["Resume-parser"]
  resume_collection = db.resumes
  if(len(required_skill)!=0 and len(one_of_skill)!=0):
    details = resume_collection.aggregate([{"$match":{"skills":{"$all":required_skill}}},{"$match":{"skills":{"$in":one_of_skill}}}])
  elif(len(required_skill)!=0):
    details = resume_collection.aggregate([{"$match":{"skills":{"$all":required_skill}}}])
  elif(len(one_of_skill)!=0):
    details = resume_collection.aggregate([{"$match":{"skills":{"$in":one_of_skill}}}])
  else:
    details = resume_collection.find({})
  return details

# sample details structure to be passed
# details = {
#  'email': 'an431999@gmail.com',
#  'location': 'Nagar',
#  'name': 'Ayush Nagar',
#  'phone': '+919717504706',
#  'skills': ['github',
#   'iit',
#   'bootstrap',
#   'mongodb',
#   'git',
#   'twitter',
#   'ml',
#   'python',
#   'mysql',
#   'twitter api',
#   'data science',
#   'api',
#   'pcm',
#   'reactjs',
#   'foundation',
#   'rest',
#   'nlp',
#   'nodejs',
#   'pvr',
#   'google',
#   'c++',
#   'flask',
#   'it',
#   'angular',
#   'dps']}

# insert new resume that is parsed
# resume_id = insert_resume(details)

# find resume by email id
# email_searched_resumes = find_resume({"email":"an431999@gmail.com"})
# for x in email_searched_resumes:
#   print(x) 

# required + one of the following skills case
# y = find_resume_by_skill(required_skill = ['nodejs'],one_of_skill=['reactjs','angular','vuejs'])

# required skills case
# y = find_resume_by_skill(required_skill = ['nodejs'])

# one of the following skills case
# y = find_resume_by_skill(one_of_skill=['reactjs','angular','vuejs'])
