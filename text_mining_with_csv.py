from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, SentimentOptions, EntitiesOptions
import scrape_parse
import csv
import json
import os


# these functions will be needed for the keywords frequency graph
def sorting_on_count(a):
    return a['count']


def sorting_on_sentiment(a):
    return a['sentiment']


# set up services
authenticator = IAMAuthenticator('rcXs4WvKrUtItOK0P1fv0mGGAC5ZfRth0ZNQWM17NIUT')
NLU = NaturalLanguageUnderstandingV1(version='2020-08-01', authenticator=authenticator)

NLU.set_service_url(
    "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2acea4e4-9e41-400b-b6a1"
    "-a27c3c7c608c")

input_files = []
classes_listed = []
illegal_types = ["Major", "AcademicStanding", "Quantity"]
illegal_subtypes = ["Freshman", "Sophomore", "Junior", "Senior", "Student", "Faculty"]

# used to get input files for later on
with os.scandir('./Sample_Class_CSV_Files') as it:
    for entry in it:
        print(entry.name)
    temp = input("Select the files you want to use: ")
    while temp != "":
        input_files.append(temp)
        temp = input()

# now loop through the input files that we get and perform operations on those inputs
while input_files:
    # variables used
    valuable = []
    needs_improvement = []
    valuable_keywords = []
    needs_improvement_keywords = []
    add = []
    sentiment_score = 0
    entities_valuables = []
    entities_needs_improvement = []
    # store the entity scores and counts in a list -> first value is sentiment, second value is count
    entities_scores = {
        'Course':
            {
                'NONE': [0, 0], 'Material': [0, 0], 'Pacing': [0, 0], 'Difficulty': [0, 0], 'Resources': [0, 0],
                'Timing': [0, 0], 'Grading': [0, 0], 'Location': [0, 0], 'TeachingStyle': [0, 0], 'Workload': [0, 0]
            },
        'Lecture':
            {
                'NONE': [0, 0], 'Material': [0, 0], 'Pacing': [0, 0], 'Timing': [0, 0],
                'Difficulty': [0, 0], 'Location': [0, 0], 'TeachingStyle': [0, 0], 'Resources': [0, 0]
            },
        'Recitation':
            {
                'NONE': [0, 0], 'Material': [0, 0], 'Pacing': [0, 0], 'Timing': [0, 0], 'Difficulty': [0, 0],
                'Resources': [0, 0], 'Grading': [0, 0], 'Location': [0, 0], 'TeachingStyle': [0, 0], 'Workload': [0, 0]
            },
        'Exams':
            {
                'NONE': [0, 0], 'Material': [0, 0], 'Pacing': [0, 0], 'Timing': [0, 0], 'Workload': [0, 0],
                'Grading': [0, 0],
                'Difficulty': [0, 0], 'Location': [0, 0], 'TeachingStyle': [0, 0], 'Resources': [0, 0]
            },
        'Lab':
            {
                'NONE': [0, 0], 'Material': [0, 0], 'Pacing': [0, 0], 'Difficulty': [0, 0], 'Resources': [0, 0],
                'Timing': [0, 0], 'Grading': [0, 0], 'Location': [0, 0], 'TeachingStyle': [0, 0], 'Workload': [0, 0]
            },
        'Projects':
            {
                'NONE': [0, 0], 'Material': [0, 0], 'Pacing': [0, 0], 'Difficulty': [0, 0],
                'Resources': [0, 0], 'Timing': [0, 0], 'Grading': [0, 0], 'Workload': [0, 0]
            },
        'Homework':
            {
                'NONE': [0, 0], 'Material': [0, 0], 'Difficulty': [0, 0], 'Workload': [0, 0],
                'Resources': [0, 0], 'Timing': [0, 0], 'Grading': [0, 0]
            },
        'Contact':
            {
                'NONE': [0, 0], 'Resources': [0, 0], 'Difficulty': [0, 0],
                'Timing': [0, 0], 'TeachingStyle': [0, 0], 'Location': [0, 0]
            },
        'Person':
            {'Professor': [0, 0], 'TeachingAssistant': [0, 0]}
    }

    # this will allow us to start reading and grabbing information from the CSV files
    with open('./Sample_Class_CSV_Files/' + input_files[0], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["TYPE"] == "Valuable":
                valuable.append(row["COMMENT"])
            elif row["TYPE"] == "Needs Improvement":
                needs_improvement.append(row["COMMENT"])
    # end reading and grabbing of information from the file

    # start the parsing of the information from the file
    # looking through all of the valuable comments of the course
    for i in valuable:
        print(i)
        print('\n')
        if len(i) == 1:
            continue
        # this is for the calculation of the sentiment score for the course using the valuable section
        sentiment_valuable_response = NLU.analyze(
            text=i,
            features=Features(sentiment=SentimentOptions()),
            language="en").get_result()
        print(json.dumps(sentiment_valuable_response['sentiment']['document']["score"], indent=1))
        # use Ervin's part for the averaging to get an average sentiment score for the valuables of the course
        add.append(sentiment_valuable_response['sentiment']['document']["score"])
        # now get all of the keywords in the valuables section of the input
        valuable_keywords_response = NLU.analyze(
            text=i,
            features=Features(keywords=KeywordsOptions(limit=20, sentiment=True)),
            language='en').get_result()
        print(json.dumps(valuable_keywords_response['keywords'], indent=2))
        # store these keywords in for later use
        for entry in valuable_keywords_response['keywords']:
            valuable_keywords.append({'keyword': entry['text'],
                                      'sentiment': entry['sentiment']['score'],
                                      'count': entry['count']})
        print("\n")
        # look for the entities in the valuable section of the input
        valuable_entities_response = NLU.analyze(
            text=i,
            features=Features(entities=EntitiesOptions(sentiment=True, model='644c43e1-f089-414c-bb2c-a1bcc1c130e5')),
        language='en').get_result()
        print(json.dumps(valuable_entities_response['entities'], indent=2))
        # now store the entities from the valuable section into the entities_valuable data structure
        for entry in valuable_entities_response['entities']:
            entities_valuables.append({'name': entry['text'],
                                       'type': entry['type'],
                                       'subtype': entry['disambiguation']['subtype'][0],
                                       'count': entry['count'],
                                       'sentiment': entry['sentiment']['score']})
        print("\n")

    # looking through all of the keywords in the needs improvement section of the course
    for i in needs_improvement:
        print(i)
        print('\n')
        if len(i.split()) == 1:
            continue
        # this is for the calculation of the sentiment score for the course using the needs improvement section
        sentiment_needs_improvement_response = NLU.analyze(
            text=i,
            features=Features(sentiment=SentimentOptions()),
            language="en").get_result()
        print(json.dumps(sentiment_needs_improvement_response['sentiment']['document']["score"], indent=1))
        # using Ervin's part to calculate a score for the needs improvement section of the course
        add.append(sentiment_needs_improvement_response['sentiment']['document']["score"])
        needs_improvement_keywords_response = NLU.analyze(
            text=i,
            features=Features(keywords=KeywordsOptions(limit=20, sentiment=True)),
            language='en').get_result()
        print(json.dumps(needs_improvement_keywords_response['keywords'], indent=2))
        for entry in needs_improvement_keywords_response['keywords']:
            needs_improvement_keywords.append({'keyword': entry['text'],
                                               'sentiment': entry['sentiment']['score'],
                                               'count': entry['count']})
        # look for the entities in the needs improvement section of the input
        needs_improvement_entities_response = NLU.analyze(
            text=i,
            features=Features(entities=EntitiesOptions(sentiment=True, model='644c43e1-f089-414c-bb2c-a1bcc1c130e5')),
        language='en').get_result()
        print(json.dumps(needs_improvement_entities_response['entities'], indent=2))
        # now store the entities from the valuable section into the entities_valuable data structure
        for entry in needs_improvement_entities_response['entities']:
            entities_needs_improvement.append({'name': entry['text'],
                                               'type': entry['type'],
                                               'subtype': entry['disambiguation']['subtype'][0],
                                               'count': entry['count'],
                                               'sentiment': entry['sentiment']['score']})
        print("\n")

    for element in add:
        sentiment_score = sentiment_score + element
    sentiment_score = sentiment_score / len(add)
    print("sentiment average = ", sentiment_score)
    # storing the sentiment score in the dataa structure for the class

    # section to check to see if there are multiple entries of the same text in the list
    temp = []
    # this list will take all the keywords in valuable_keywords
    key_num_list = [dictionaries['keyword'] for dictionaries in valuable_keywords]

    for entry in valuable_keywords:
        # if the keyword in entry has more than one occurrence in the list that we
        # created before, loop through the list to see all the occurrences and add
        # up the corresponding sections
        if key_num_list.count(entry['keyword']) > 1:
            # initialize an entry to have this template
            i = {'keyword': entry['keyword'],
                 'sentiment': 0,
                 'count': 0}
            # loop through valuable_keywords to find the multiple occurrences
            for entry2 in valuable_keywords:
                # if you find the occurrence, update it
                if entry2['keyword'] == entry['keyword']:
                    i = {'keyword': entry2['keyword'],
                         'sentiment': i['sentiment'] + entry2['count'] * entry2['sentiment'],
                         'count': i['count'] + entry2['count']}
                else:
                    # move on, since you couldn't find the keyword yet
                    continue
            # at the very end, add it to the temp list if it wasn't added already
            if i not in temp:
                temp.append(i)
        else:
            # if you only have one occurrence, just put it into the list
            temp.append({'keyword': entry['keyword'],
                         'sentiment': entry['sentiment'],
                         'count': entry['count']})
    # normalize the sentiment values now
    valuable_keywords.clear()
    for entry in temp:
        entry = {'keyword': entry['keyword'],
                 'sentiment': entry['sentiment'] / (entry['count']),
                 'count': entry['count']}
        valuable_keywords.append(entry)
    # this will allow us to sort the frequency based on the count and sentiment
    # First order based on sentiment. Since it would order based on sentiment,
    # if we later decided to order by count and if count is the same, it will
    # retain the previous order that we had
    valuable_keywords.sort(key=sorting_on_sentiment, reverse=True)
    # order by count now
    valuable_keywords.sort(key=sorting_on_count, reverse=True)
    print("\n\n\n\n")
    print(json.dumps(valuable_keywords, indent=2))
    print("\n")
    # this is the valuable_keywords is the list that we will be using to output to the graphs

    temp = []
    # this list will take all the keywords in needs_improvement_keywords
    key_num_list = [dictionaries['keyword'] for dictionaries in needs_improvement_keywords]

    for entry in needs_improvement_keywords:
        # if the keyword in entry has more than one occurrence in the list that we
        # created before, loop through the list to see all the occurrences and add
        # up the corresponding sections
        if key_num_list.count(entry['keyword']) > 1:
            # initialize an entry to have this template
            i = {'keyword': entry['keyword'],
                 'sentiment': 0,
                 'count': 0}
            # loop through needs_improvement_keywords to find the multiple occurrences
            for entry2 in needs_improvement_keywords:
                # if you find the occurrence, update it
                if entry2['keyword'] == entry['keyword']:
                    i = {'keyword': entry2['keyword'],
                         'sentiment': i['sentiment'] + entry2['count'] * entry2['sentiment'],
                         'count': i['count'] + entry2['count']}
                else:
                    # move on, since you couldn't find the keyword yet
                    continue
            # at the very end, add it to the temp list if it wasn't added already
            if i not in temp:
                temp.append(i)
        else:
            # if you only have one occurrence, just put it into the list
            temp.append({'keyword': entry['keyword'],
                         'sentiment': entry['sentiment'],
                         'count': entry['count']})
    # normalize the sentiment values now
    needs_improvement_keywords.clear()
    for entry in temp:
        entry = {'keyword': entry['keyword'],
                 'sentiment': entry['sentiment'] / (entry['count']),
                 'count': entry['count']}
        needs_improvement_keywords.append(entry)
    # this will allow us to sort the frequency based on the count and sentiment
    # First ord- er based on sentiment. Since it would order based on sentiment,
    # if we later decided to order by count and if count is the same, it will
    # retain the previous order that we had
    needs_improvement_keywords.sort(key=sorting_on_sentiment, reverse=False)
    # order by count now
    needs_improvement_keywords.sort(key=sorting_on_count, reverse=True)
    print("\n\n\n\n")
    print(json.dumps(needs_improvement_keywords, indent=2))
    print("\n")
    # needs_improvement_keywords is final list

    # now it's time to store the needed information for the entities
    # first look into what the valuable entities list has and use that information
    for entry in entities_valuables:
        entity_type = entry['type']
        entity_subtype = entry['subtype']
        if entity_type == 'Person' and entity_subtype == 'NONE':
            continue
        if (entity_type not in illegal_types) and (entity_subtype not in illegal_subtypes):
            # update the sentiment scores for the entity types and subtypes
            entities_scores[entity_type][entity_subtype][0] = entities_scores[entity_type][entity_subtype][0] + entry[
                'sentiment'] * entry['count']
            # update the count for the entity types and subtypes
            entities_scores[entity_type][entity_subtype][1] = entities_scores[entity_type][entity_subtype][1] + entry[
                'count']
    # now look into what the needs improvement entities list has and use that information
    for entry in entities_needs_improvement:
        entity_type = entry['type']
        entity_subtype = entry['subtype']
        if entity_type == 'Person' and entity_subtype == 'NONE':
            continue
        if (entity_type not in illegal_types) and (entity_subtype not in illegal_subtypes):
            # update the sentiment scores for the entity types and subtypes
            entities_scores[entity_type][entity_subtype][0] = entities_scores[entity_type][entity_subtype][0] + \
                                                              entry['sentiment'] * entry['count']
            # update the count for the entity types and subtypes
            entities_scores[entity_type][entity_subtype][1] = entities_scores[entity_type][entity_subtype][1] + \
                                                              entry['count']

    # now put in all of that information into the classes_listed data structure
    classes_listed.append({'name_of_class': input_files[0].split("_")[0],
                           'class_time': input_files[0].split("_")[1].split(".")[0],
                           'average_sentiment_score': sentiment_score,
                           'valuable_keywords': valuable_keywords,
                           'needs_improvement_keywords': needs_improvement_keywords,
                           'entities_scores': entities_scores
                           })

    # remove the file we finished using from the input_files list
    input_files.pop(0)
print("YOU HAVE REACHED THE END OF THE SIMULATION\n ")
