import pandas as pd
import json
import warnings

warnings.filterwarnings('ignore')
import re
import nltk
from nltk.corpus import stopwords
import string

import joblib
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier


def cleanResume(resumeText):
    resumeText = re.sub('[%s]' % re.escape("""!"$%&'()*,-/:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText


def getData():
    resumeDataSet = pd.read_csv('Datasets/new_dataset_of_resume_skills1.csv')
    resumeDataSet['cleaned_resume_skills'] = ''
    resumeDataSet['cleaned_resume_skills'] = resumeDataSet.Resume.apply(lambda x: cleanResume(x))
    return resumeDataSet


def encoding(resumeDataSet):
    le = LabelEncoder()
    resumeDataSet['Category'] = le.fit_transform(resumeDataSet['Category'])
    joblib.dump(le, 'models/labelEncoder.pkl')


def vectorizing():
    skillDataSet = pd.read_csv('Datasets/new_dataset_of_resume_skills1.csv')

    word_vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words='english')
    word_vectorizer.fit(skillDataSet['skills'].values)
    WordFeatures = word_vectorizer.transform(skillDataSet['skills'].values)

    joblib.dump(word_vectorizer, 'models/wordVectorizer.pkl')
    # return WordFeatures


def trainModel(X, Y):
    x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=4, test_size=0.25)
    model = KNeighborsClassifier(n_neighbors=10).fit(X, Y)
    joblib.dump(model, 'models/knn.pkl')


def printAccuracy(x_test, y_test):
    model = joblib.load("models/knn.pkl")
    print('Accuracy of KNN :- {:.2f}'.format(model.score(x_test, y_test)))


if __name__ == "__main__":
    # Get data
    resumeDataSet = getData()

    # Cleaned Resume values
    reqText = resumeDataSet['cleaned_resume_skills'].values

    # Encoding the Categories
    # encoding(resumeDataSet)

    # The encoded required category values
    reqTarget = resumeDataSet['Category']

    # For TF-IDF
    # vectorizing()
    wordVec = joblib.load('models/wordVectorizer.pkl')
    wordFeatures = wordVec.transform(reqText)

    # Model Training
    # trainModel(wordFeatures, reqTarget)

    x_train, x_test, y_train, y_test = train_test_split(wordFeatures, reqTarget, random_state=4, test_size=0.25)
    printAccuracy(x_test, y_test)
