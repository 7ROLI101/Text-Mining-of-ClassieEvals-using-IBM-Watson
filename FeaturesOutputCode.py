from ibm_watson import NaturalLanguageUnderstandingV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features,EmotionOptions,CategoriesOptions
import scrape_parse
import csv
import json
import os

authenticator = IAMAuthenticator('rcXs4WvKrUtItOK0P1fv0mGGAC5ZfRth0ZNQWM17NIUT')
NLU = NaturalLanguageUnderstandingV1(version = '2020-08-01', authenticator = authenticator)

NLU.set_service_url("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2acea4e4-9e41-400b-b6a1-a27c3c7c608c")

valuable = []
needs_improvement = []


with os.scandir('./Sample_Class_CSV_Files') as it:
    for entry in it:
        print(entry.name)
    file = input("Select a file you want to use: ")

with open('./Sample_Class_CSV_Files/' + file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["TYPE"] == "Valuable":
            valuable.append(row["COMMENT"])
        elif row["TYPE"] == "Needs Improvement":
            needs_improvement.append(row["COMMENT"])
    #prints the valuable comments into a output file called valuableOutput.txt
    valuableOutputFile = open("valuableOutput.txt","w+")
    valuableOutputFile.write("This is for Positive Comments")
    valuableOutputFile.write("\n")
    for i in valuable:
        print(i)
        print("\n")
        response = NLU.analyze(text = i, features = Features(categories = CategoriesOptions(explanation= True, limit = 3))).get_result()
        print(json.dumps(response,indent = 1))
        print("\n")
        valuableOutputFile.write(json.dumps(response,indent = 1))
        valuableOutputFile.write("\n")
    #prints the needs_improvement comments into a output file called needsImprovementOutput.txt
    needsImprovementOutputFile = open("needsImprovementOutput.txt","w+")
    needsImprovementOutputFile.write("This is for Negative Comments" "\n")    
    for j in needs_improvement:
        print(j)
        print("\n")
        response = NLU.analyze(text = i, features = Features(categories = CategoriesOptions(explanation= True, limit = 3))).get_result()
        print(response)
        print("\n")
        needsImprovementOutputFile.write(json.dumps(response,indent = 1))
        needsImprovementOutputFile.write("\n")   