import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
import joblib
import sys
from database_functionalities import insertIntoCategoryCollection

def getVectorizer(skills):
    try:
        skillsSet=[]
        for skill in skills:
            skill=skill.replace(" ","")
            skillsSet.append(skill)

        # ... skillSet=["machinelearning","java","c++","nodejs"]
        vectorizer = CountVectorizer(tokenizer=lambda txt: txt.split())
        # ... Joined skills string  = "machinelearning java c++ nodejs"
        vocabulary = vectorizer.fit([" ".join(skillsSet)])
        # print(vocabulary.get_feature_names())
        return vectorizer
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def removePunctuation(s):
    try:
        newS=""
        punctuations = '''!()|-[]{};:'"\,<>./?@$%^&_~'''
        for i in s:
            if(i not in punctuations):
                newS=newS+i
        return newS
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return ""
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return ""



def readCategory():
    try:
        dictCat={}
        idx=0
        data=pd.read_csv("./Datasets/category.csv")
        category=data["category"].tolist()
        distinct_category=list(set(category))
        distinct_category.sort()
        for i in distinct_category:
            dictCat[i]=idx
            idx=idx+1
        # ... Dict category has the format ==> {"software engineer jobs" -> 57}
        #To insert the category into category collection uncomment the below line.. ..
        # insertIntoCategoryCollection(dictCat)
        return distinct_category,dictCat
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return [],{}
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return [],{}

def cleanSKillColumn(skills):
    try:
        cleaned=[]
        for skill in skills:
            temp=skill.replace(","," ").replace("/"," ").replace("."," ").replace(" ","").lower()
            cleaned.append(temp)
        return cleaned
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return []
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return []

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
    # ... dict = {57 -> "Software Engineer Jobs"}
    # ... cat = ["Softeare enginerr jobs" ,"Softeare enginerr jobs","Java jobs"]
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


# def trainKnn():
#     try:
#         category, dictCategory = readCategory()
#         skillSet = getSkillSet()
#         vectorizer = getVectorizer(skillSet)
#         data = pd.read_csv("./Datasets/jobs_skills.csv")
#
#         X, Y = getMatrixInput(data["skills"].tolist(), data["category"].tolist(), dictCategory, vectorizer)
#
#         # ... X=[
#         #     [1,1,1,1,1,1],
#         #     [1,0,1,0,1,1]
#         # ]
#         # ... Y=[57,40]
#
#         X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, shuffle=True)
#         knn = KNeighborsClassifier(n_neighbors=9)
#         knn.fit(X, Y)
#         joblib.dump(knn, './models/knnClassifier.pkl')
#
#     except ValueError:
#         print("Value Error :",sys.exc_info()[0])
#         raise
#     except:
#         print("Unexpected error:", sys.exc_info()[0])
#         raise

def getClassification(skills):
    try:
        dictEncodedCat,Cat=getStoredEncodedClasses()
        # ... dictEncodedCat={57 -> "Software Engineer Jobs"}
        knn=joblib.load("./models/knnClassifier.pkl")
        skillSet = getSkillSet()
        vectorizer=getVectorizer(skillSet)
        array = cleanSKillColumn(skills)
        vect = vectorizer.transform([" ".join(array)]).toarray()
        ans = knn.predict(vect)
        # print(ans)
        dist, ind = knn.kneighbors(vect)
        cat_list=[]

        for i in range(0,3):
            # print(i,Cat[ind[0][i]])
            cat_list.append(Cat[ind[0][i]].replace("Jobs","Profile"))
        # print(dictEncodedCat[ans[0]])
        cat_list.append(dictEncodedCat[ans[0]].replace("Jobs","Profile"))
        return list(set(cat_list))
    except ValueError:
        print("Value Error :",sys.exc_info()[0])
        return []
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return []

if __name__ == "__main__":
    print(getClassification(["reactjs","javascript","python","C++"]))
