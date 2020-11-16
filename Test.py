from ibm_watson import NaturalLanguageUnderstandingV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features,EmotionOptions,CategoriesOptions
import scrape_parse
import csv
import json

authenticator = IAMAuthenticator('rcXs4WvKrUtItOK0P1fv0mGGAC5ZfRth0ZNQWM17NIUT')
NLU = NaturalLanguageUnderstandingV1(version = '2020-08-01', authenticator = authenticator)

NLU.set_service_url("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2acea4e4-9e41-400b-b6a1-a27c3c7c608c")

positive = []
negative = []


with open('ESE380-01FALL2018.csv', newline = '') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: 
        if row["TYPE"] == "Valuable":
            positive.append(row["COMMENT"]) 
        elif row["TYPE"] == "Needs Improvement":
            negative.append(row["COMMENT"])
        
    for i in positive:
        print(i)
        print("\n")
        response = NLU.analyze(text = i, features = Features(categories = CategoriesOptions(explanation= True, limit = 3))).get_result()
        print(json.dumps(response,indent = 1))
        print("\n")
        
    for j in negative:
        print(j)
        print("\n")
        response = NLU.analyze(text = i, features = Features(categories = CategoriesOptions(explanation= True, limit = 3))).get_result()
        print(response)
        print("\n")
        