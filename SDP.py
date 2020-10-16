# needed for parsing the input file
from bs4 import BeautifulSoup
# needed for reg expressions for the find functions in BeautifulSoup4
import re
# needed in order to make requests to ClassieEvals
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
import json 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

api_key = 'rcXs4WvKrUtItOK0P1fv0mGGAC5ZfRth0ZNQWM17NIUT'
url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2acea4e4-9e41-400b-b6a1-a27c3c7c608c'
authenticator = IAMAuthenticator(api_key)
service = NaturalLanguageUnderstandingV1(version = '2020-10-14',authenticator= authenticator)
service.set_service_url(url)


with requests.Session() as session:
    # THIS IS THE PART WHERE WE USE REQUESTS IN ORDER TO ACCESS CLASSIEEVALS
    j = session.get("https://classie-evals.stonybrook.edu/")
    username = input("Enter in your username: ")
    password = input("Enter in your password: ")
    payload = {'j_username': username,
               'j_password': password,
               '_eventId_proceed': ''}
    k = session.post("https://sso.cc.stonybrook.edu/idp/profile/cas/login?execution=e1s1", data=payload)
    l = session.get("https://classie-evals.stonybrook.edu/")
    class_num = input("Enter in the class you want to search for: ")
    season = input("Enter in the season you want to look at: ").title().strip()
    year = input("Enter in the year you want to look for: ")
    times_to_code = {
        'Summer 2020': "1206", 'Spring 2020': "1204", 'Winter 2020': "1201", 'Fall 2019': "1198", 'Summer 2019': "1196",
        'Spring 2019': "1194", 'Winter 2019': "1191", 'Fall 2018': "1188", 'Summer 2018': "1186", 'Spring 2018': "1184",
        'Winter 2018': "1181", 'Fall 2017': "1178", 'Summer 2017': "1176", 'Spring 2017': "1174", 'Winter 2017': "1171",
        'Fall 2016': "1168", 'Summer 2016': "1166", 'Spring 2016': "1164", 'Winter 2016': "1161", 'Fall 2015': "1158",
        'Summer 2015': "1156", 'Spring 2015': "1154", 'Winter 2015': "1151", 'Summer 2014': "1146",
        'Spring 2014': "1144"}
    time = times_to_code[season + ' ' + year]
    input_classie = {'SearchKeyword': 'ese+' + class_num,
                     'SearchTerm': time}

    n = session.get("https://classie-evals.stonybrook.edu/" + "?SearchKeyword="
                    + input_classie['SearchKeyword'] + "&SearchTerm=" + input_classie['SearchTerm'])
    classes_chosen = BeautifulSoup(n.text, 'html.parser').find('tbody').find_all('tr')
    classes_found = [{'code': chosen.contents[1].a.string,
                      'name': chosen.contents[3].string.replace("\r", " ").replace("\n", " ").strip(),
                      'instructor': chosen.contents[5].a.string,
                      'website': chosen.contents[1].a['href']
                      } for chosen in classes_chosen]
    # print(classes_found)
    print("Here is what was found:\n")
    print("Class Code #\t\t Class Name \t\t  Class Instructor")
    for classes in classes_found:
        print(classes['code'] + "\t\t" + classes['name'] + "\t\t" + classes['instructor'])
    class_code = input("Enter in a class code you want to use: ")
    # This part provides error in input checking
    # while class_code not in classes_found:
    #     print("\nERROR: INVALID CLASS CODE PROVIDED")
    #     for classes in classes_found:
    #         print(classes['code'] + "\t\t" + classes['name'] + "\t\t" + classes['instructor'])
    #     class_code = input("\nEnter in a class code you want to use: ")

    for classes in classes_found:
        if classes['code'] == class_code.strip().upper():
            web_url = "https://classie-evals.stonybrook.edu/" + classes['website']
            l = session.get(web_url)
            # END OF ACCESSING THE INTERNET WITH REQUESTS

            # PARSING OF THE FILE all of this code is for the part where we open up the file and see what are the
            # possible positives(aka the section What was valuable about this course? on ClassieEvals) and what are
            # the possible negatives(aka the section What could be improved about this course? on Classie Evals)
            j = BeautifulSoup(l.content, 'html.parser')
            # this is for the class details
            class_description = j.find('section', 'bg-black basic-hero overlay-none cozy').text.split("\n")

            temp = []
            for x in class_description:
                if x == '':
                    continue
                else:
                    x = x.strip()
                    if x == '':
                        continue
                    else:
                        temp.append(x)
            class_description = temp

            class_properties = {'class_code': class_description[0],
                                'time': class_description[1],
                                'class_type': class_description[2].title(),
                                'class_name': class_description[3],
                                'professors': class_description[4].replace(" and ", ", ").split(", ")}
            print(class_properties)

            # finding the section with the valuable aspects of the course
            found_pos = j.find('h4', string=re.compile('What was valuable about this course?'))
            # look for the next section block
            found_pos = found_pos.find_next('ul')
            # within the section for the valuable aspects of the code, look for all the <li> tags
            valuables = found_pos.find_all('li')
            # store the comments into the positive variable and strip off leading whitespace
            positives = [valuable.text.strip() for valuable in valuables]
            class_properties['positives'] = positives

            # finding the section with the needs improvement aspects of the course
            found_neg = j.find('h4', string=re.compile('What could be improved about this course?'))
            # finding the next section block
            found_neg = found_neg.find_next('ul')
            # within the section for the valuable aspects of the code, look for all the <li> tags
            needs_improvements = found_neg.find_all('li')
            # store the comments into the negative variable and strip off leading whitespace
            negatives = [needs_improvement.text.strip() for needs_improvement in needs_improvements]
            class_properties['negatives'] = negatives

            # section for printing everything out for debugging
            print("\n")
            print("Here are the comments for what people thought was valuable about the course:")
            print("\n")
            for positive in positives:
                print("• " + positive + "\n")
            print("\n")
            print("Here are the comments for what people thought the course needed improvement:")
            print("\n")
            for negative in negatives:
                print("• " + negative + "\n")
            print("\n")
            break
            # END OF PARSING OF THE FILE
