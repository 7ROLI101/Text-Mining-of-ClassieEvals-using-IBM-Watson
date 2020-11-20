from ibm_watson import NaturalLanguageUnderstandingV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features,EmotionOptions,CategoriesOptions
import scrape_parse
import csv
import json
import os
import os.path


authenticator = IAMAuthenticator('rcXs4WvKrUtItOK0P1fv0mGGAC5ZfRth0ZNQWM17NIUT')
NLU = NaturalLanguageUnderstandingV1(version = '2020-08-01', authenticator = authenticator)

NLU.set_service_url("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2acea4e4-9e41-400b-b6a1-a27c3c7c608c")

valuable = []
needs_improvement = []


with os.scandir('./Sample_Class_CSV_Files') as it:
    for entry in it:
        print(entry.name)
    file = input("Select a file you want to use: ")
    fileName = file.split(".")
    print(fileName[0])
    
with open('./Sample_Class_CSV_Files/' + file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["TYPE"] == "Valuable":
            valuable.append(row["COMMENT"])
        elif row["TYPE"] == "Needs Improvement":
            needs_improvement.append(row["COMMENT"])
    #prints the valuable comments into a output file called valuableOutput.txt
    OutputFile = open(fileName[0] + "_Emotions.txt","a+")
    for i in valuable:
        print(i)
        print("\n")
        OutputFile.write(i)
        OutputFile.write("\n")
        response = NLU.analyze(text = i, features = Features(emotion = EmotionOptions(document=True))).get_result()
        print(json.dumps(response["emotion"],indent = 2))
        print("\n")
        OutputFile.write(json.dumps(response["emotion"],indent = 2))
        OutputFile.write("\n")
    #prints the needs_improvement comments into a output file called needsImprovementOutput.txt 
    for j in needs_improvement:
        print(j)
        print("\n")
        OutputFile.write(j)
        OutputFile.write("\n")
        response = NLU.analyze(text = j, features = Features(emotion = EmotionOptions(document=True))).get_result()
        print(json.dumps(response["emotion"],indent = 2))
        print("\n")
        OutputFile.write(json.dumps(response["emotion"],indent = 2))
        OutputFile.write("\n")   