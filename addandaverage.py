from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import scrape_parse
import csv
import json
import os

authenticator = IAMAuthenticator('rcXs4WvKrUtItOK0P1fv0mGGAC5ZfRth0ZNQWM17NIUT')
NLU = NaturalLanguageUnderstandingV1(version = '2020-08-01', authenticator = authenticator)

NLU.set_service_url("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2acea4e4-9e41-400b-b6a1-a27c3c7c608c")

valuable = []
needs_improvement = []
add = []
total=0
average=0

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
    for i in valuable:
        response = NLU.analyze(text = i, features = Features(sentiment = SentimentOptions()),language="en").get_result()
        print(json.dumps(response['sentiment']['document']["score"],indent = 1))
        add.append(response['sentiment']['document']["score"])

    for i in needs_improvement:
        response = NLU.analyze(text = i, features = Features(sentiment = SentimentOptions()),language="en").get_result()
        print(json.dumps(response['sentiment']['document']["score"],indent = 1))
        add.append(response['sentiment']['document']["score"])

    for ele in add:
        total = total + ele
    average = total/len(add)
    print("sentiment average = ",average)