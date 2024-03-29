from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, SentimentOptions
import scrape_parse
import json

# these functions will be needed for the keywords frequency graph


def sorting_on_count(a):
    return a['count']


def sorting_on_sentiment(a):
    return a['sentiment']


# set up services
authenticator = IAMAuthenticator('rcXs4WvKrUtItOK0P1fv0mGGAC5ZfRth0ZNQWM17NIUT')
NLU = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)
NLU.set_service_url(
    'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2acea4e4-9e41-400b-b6a1'
    '-a27c3c7c608c')

# variables used
valuable = []
needs_improvement = []
valuable_keywords = []
needs_improvement_keywords = []
add = []
sentiment_score = 0

# this is where we edit the code to introduce what we need
scrape_parse.input_user_info()
classie = scrape_parse.inputClass()
classie.set_input_class_info()
classie.set_class_info()
class_name = classie.get_class_code()
class_time = str(classie.get_class_season()).upper() + str(classie.get_class_year())
valuable = classie.get_positive_comments()
needs_improvement = classie.get_negative_comments()

for i in valuable:
    print(i)
    print('\n')
    if len(i) == 1:
        continue
    sentiment_valuable_response = NLU.analyze(
        text=i,
        features=Features(sentiment=SentimentOptions()),
        language="en").get_result()
    print(json.dumps(sentiment_valuable_response['sentiment']['document']["score"], indent=1))
    add.append(sentiment_valuable_response['sentiment']['document']["score"])
    valuable_keywords_response = NLU.analyze(
        text=i,
        features=Features(keywords=KeywordsOptions(limit=20, sentiment=True)),
        language='en').get_result()
    print(json.dumps(valuable_keywords_response['keywords'], indent=2))
    for entry in valuable_keywords_response['keywords']:
        valuable_keywords.append({'keyword': entry['text'],
                                  'sentiment': entry['sentiment']['score'],
                                  'count': entry['count']})
    print("\n")

for i in needs_improvement:
    print(i)
    print('\n')
    if len(i.split()) == 1:
        continue
    sentiment_needs_improvement_response = NLU.analyze(
        text=i,
        features=Features(sentiment=SentimentOptions()),
        language="en").get_result()
    print(json.dumps(sentiment_needs_improvement_response['sentiment']['document']["score"], indent=1))
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
    print("\n")

for element in add:
    sentiment_score = sentiment_score + element
sentiment_score = sentiment_score / len(add)
print("sentiment average = ", sentiment_score)

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
                     'sentiment': i['sentiment'] + entry2['sentiment'],
                     'count': i['count'] + 1}
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
# valuable_keywords is the list that we will be using to output to the graphs
