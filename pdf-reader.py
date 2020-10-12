import textract
import re
import pandas as pd
import unidecode
def convert(fname, pages=None):
	text = textract.process(fname, method='pdfminer')
	return text

def getName(resume_content):
    name=""
    for st in resume_string:
        if(st!='' and st.lower()!='resume' and st.lower()!='cv' and st.lower()!='resume/cv' and name==""):
            name = st
            break
    return name

def getEmail(resume_content):
    email = ""
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    for st in resume_content:
        words = st.split(' ')
        for word in words:
            if(re.search(regex,word)):  
                email = word
                break
    return email

def getPhoneNumber(resume_content):
    phone = ""
    regex = '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'
    for st in resume_content:
        words = st.split(' ')
        for word in words:
            if(re.search(regex,word)):  
                phone = word
                break
    return phone

# def getLocation(resume_content):
#     regex = "^([a-zA-Z\u0080-\u024F]+(?:. |-| |'))*[a-zA-Z\u0080-\u024F]*$"
#     location = ""
#     for st in resume_content:
#         # words = st.split(' ')
#         # for word in words:
#         if(re.search(regex,st)):  
#             location = st
#             break
#     return location

def getSkills(resume_content,skills_list):
    skills = []
    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    for st in resume_content:
        words = st.split(' ')
        words = words + st.split(',')
        words = words + st.split('|')
        l = st.split()
        result = []
        for i in range(len(l) - 1):
            result.append(l[i] + ' ' + l[i+1])
        # print(result)
        words = list(set(list(set(words))+list(set(result))))
        for word in words:
            if(word.lower().strip() in skills_list or word.strip() in skills_list):  
                skills.append(word.lower().strip())
    return list(set(skills))

resume_string = convert("resumes/Ayush-resume-dxc.pdf").decode("utf-8").split('\n')
for i in range(0,len(resume_string)):
    encoded_string = resume_string[i].encode("ascii", "ignore")
    # resume_string[i].encode('ascii', 'replace')
    resume_string[i] = encoded_string.decode()
    resume_string[i] =  resume_string[i].strip()
df = pd.read_csv("data/techskill.csv")
df1 = pd.read_csv("data/techchatt.csv")
skills_list = list(df.keys())
skills_list = skills_list + list(df1.keys())
# print(skills_list)

details = {
    "name":getName(resume_string),
    "email":getEmail(resume_string),
    "phone":getPhoneNumber(resume_string),
    "skills":getSkills(resume_string,skills_list)
}

# print(resume_string)
# print()
print(details)