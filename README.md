# Setup process
* pip3 install -r requirements.txt
* python3 resume_reader.py to read and insert resumes.
* python3 resume_classification.py to classify resumes.
* All the CVs are present in **resumes_in_db** folder that are present in database.
* All the CVs that are pending to be added in database are present in **CVs** folder.
* **test_cvs** folder is to test resume upload in db.
* To access database and use database_functionalities function first use connection function to get client object of mongodb. To run a function, your first parameter in each function must be client object.