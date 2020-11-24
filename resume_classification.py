import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')
import re
import nltk
from nltk.corpus import stopwords
import string
import joblib
# from sklearn.externals import joblib
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

nltk.download('stopwords')
nltk.download('punkt')

def cleanResume(resumeText):
    resumeText = re.sub('[%s]' % re.escape("""!"$%&'()*,-/:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

def getData():

  resumeDataSet = pd.read_csv('new_dataset_of_resume_skills1.csv')
  # resumeDataSet['cleaned_resume_skills'] = ''
  # resumeDataSet['cleaned_resume_skills'] = resumeDataSet.Resume.apply(lambda x: cleanResume(x.lower()))
  
  return resumeDataSet

def topKNeighbours(y, testData,k=3):

  model = joblib.load('knn.pkl')
  le = joblib.load('labelEncoder.pkl')

  top_k = set()     # Set of unique Neighbours
  i = 1             # Predicted value will always be added to the set

  predictedValue = model.predict(testData)
  invrValue = le.inverse_transform(predictedValue)[0]
  
  top_k.add(invrValue)
  dist, ind = model.kneighbors(testData)
  # print(dist[0])
  # print(ind[0])

  for i in range(k-1) :
      top_k.add(y[ind[0][i]])
  
  return top_k

def get_category(skills):
    resumeDataSet = getData()  
    if(len(skills)==0):
      return []
    # Y == Categories without encoding
    y = resumeDataSet['Category']
    
    cleanTestData = [x.lower() for x in skills]
 
    # Transforming the test data to vector form
    wordVec = joblib.load('wordVectorizer.pkl')
    wordFeatures_testData = wordVec.transform(cleanTestData)

    # Top K categories
    topK = topKNeighbours(y,wordFeatures_testData)
    # print(topK)
    return topK

if __name__ == "__main__":

  # Get data
  resumeDataSet = getData()  

  # Y == Categories without encoding
  y = resumeDataSet['Category']
  
  # # Cleaned Resume values
  # reqText = resumeDataSet['cleaned_resume_skills'].values
  
  # # Encoding the Categories
  # encoding(resumeDataSet)

  # # The encoded required category values
  # reqTarget = resumeDataSet['Category'].values

  # # For TF-IDF
  # wordFeatures = vectorizing(reqText)

  # # Training the model
  # trainModel(wordFeatures,reqTarget)

  testData = ['reactjs', 'pvr', 'flask', 'fixing', 'it', 'rest', 'features', 'pcm', 'data science', 'c++', 'repository', 'application', 'ticketing', 'shopping', 'twitter', 'google', 'health', 'ml', 'git', 'api', 'community health', 'twitter api', 'foundation', 'badges', 'star', 'mongodb', 'refactoring', 'app', 'iit', 'bootstrap', 'dps', 'web', 'new features', 'nlp', 'cron', 'responsiveness', 'javascript', 'history', 'angular', 'waiting', 'nodejs', 'speech', 'mysql', 'github', 'python']
  cleanTestData = [x.lower() for x in testData]
 
  # Transforming the test data to vector form
  wordVec = joblib.load('wordVectorizer.pkl')
  wordFeatures_testData = wordVec.transform(cleanTestData)

  # Top K categories
  topK = topKNeighbours(y,wordFeatures_testData)
  print(topK)