from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions
import scrape_parse
import json
#set up services
authenticator = IAMAuthenticator('rcXs4WvKrUtItOK0P1fv0mGGAC5ZfRth0ZNQWM17NIUT')
NLU = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)
NLU.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2acea4e4-9e41-400b-b6a1-a27c3c7c608c')

#this is where we edit the code to introduce what we need
scrape_parse.input_user_info()
classie = scrape_parse.inputClass()
classie.set_input_class_info()
classie.set_class_info()
class_name = classie.get_class_code()
class_time = str(classie.get_class_season()).upper() + str(classie.get_class_year())
negative_comment = classie.get_negative_comments()
positive_comment = classie.get_positive_comments()

with open(str(class_name.upper()) + class_time + '_Entities.txt', mode='w', newline='') as file:
    for i in positive_comment:
        file.write(i)
        file.write('\n')
        response = NLU.analyze(
            text=i,
            features=Features(
                entities=EntitiesOptions(limit=15, sentiment=True, emotion=True))).get_result()
        file.write(json.dumps(response, indent=2))
        file.write('\n')
        file.write('\n')
    print("\n")
    for i in negative_comment:
        file.write(i)
        file.write('\n')
        response = NLU.analyze(
            text=i,
            features=Features(
                entities=EntitiesOptions(limit=15, sentiment=True, emotion=True))).get_result()
        file.write(json.dumps(response, indent=2))
        file.write('\n')
        file.write('\n')

