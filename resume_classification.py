import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
import joblib


def getVectorizer(skills):
    skillsSet=[]
    for skill in skills:
        skill=skill.replace(" ","")
        skillsSet.append(skill)
    vectorizer = CountVectorizer(tokenizer=lambda txt: txt.split())
    vocabulary = vectorizer.fit([" ".join(skillsSet)])

    # print(vocabulary.get_feature_names())
    return vectorizer


def removePunctuation(s):
    newS=""
    punctuations = '''!()|-[]{};:'"\,<>./?@$%^&_~'''
    for i in s:
        if(i not in punctuations):
            newS=newS+i
    return newS

def readCategory():
    dictCat={}
    idx=0
    data=pd.read_csv("./Datasets/category.csv")
    category=data["category"].tolist()
    distinct_category=list(set(category))
    distinct_category.sort()
    for i in distinct_category:
        dictCat[i]=idx
        idx=idx+1
    print(dictCat)
    return distinct_category,dictCat

def cleanSKillColumn(skills):
  cleaned=[]
  for skill in skills:
    temp=skill.replace(","," ").replace("/"," ").replace("."," ").replace(" ","").lower()
    cleaned.append(temp)
  return cleaned

def getMatrixInput(skills,test_cat,dictCategory,vectorizer):
  mat=[]
  cat=[]
  for idx in range(0,len(skills)):
    arr=eval(skills[idx])
    if(len(arr)!=0):
      arr=cleanSKillColumn(arr)
      temp=vectorizer.transform([" ".join(arr)]).toarray()
      mat.append(temp[0])
      cat.append(dictCategory[test_cat[idx]])
  return mat,cat


def getStoredEncodedClasses():
    data=pd.read_csv("./Datasets/encoded_category.csv")
    enc_cat=data["encoded_category"].tolist()
    cat=data["category"].tolist()
    dict={}
    for idx in range(0,len(cat)):
        dict[enc_cat[idx]]=cat[idx]
    return dict,cat

def getSkillSet():
    data=pd.read_csv("./Datasets/new_skills.csv")
    skills_data=data["skills"].tolist()
    lower_skills=[]
    for skills in skills_data:
        if(skills==skills):
            skills=removePunctuation(skills)
            skills=skills.lower()
            lower_skills.append(skills)
    return lower_skills


def getEncodedCat(test_cat,dictCategory):
    arr=[]
    for i in test_cat:
        arr.append(dictCategory[i])
    return arr

def inverse(i,dictCategory):
  for key,value in dictCategory.items():
    if(value==i):
      return key

def trainKnn():
    category, dictCategory = readCategory()
    skillSet = getSkillSet()
    vectorizer = getVectorizer(skillSet)
    data = pd.read_csv("./Datasets/jobs_skills.csv")
    X, Y = getMatrixInput(data["skills"].tolist(), data["category"].tolist(), dictCategory, vectorizer)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, shuffle=True)
    knn = KNeighborsClassifier(n_neighbors=9)
    knn.fit(X_train, y_train)
    joblib.dump(knn, './models/knnClassifier.pkl')

def getClassification(skills):
    dictEncodedCat,Cat=getStoredEncodedClasses()
    data = pd.read_csv("./Datasets/jobs_skills.csv")
    knn=joblib.load("./models/knnClassifier.pkl")
    skillSet = getSkillSet()
    vectorizer=getVectorizer(skillSet)
    array = cleanSKillColumn(skills)
    vect = vectorizer.transform([" ".join(array)]).toarray()
    ans = knn.predict(vect)
    print(ans)
    dist, ind = knn.kneighbors(vect)
    cat_list=[]
    # print(dist[0])

    for i in range(0,3):
        print(i,Cat[ind[0][i]])
        cat_list.append(Cat[ind[0][i]].replace("Jobs","Profile"))
    print(dictEncodedCat[ans[0]])
    cat_list.append(dictEncodedCat[ans[0]].replace("Jobs","Profile"))
    return list(set(cat_list))


