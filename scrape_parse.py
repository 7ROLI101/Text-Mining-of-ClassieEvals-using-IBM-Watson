# needed for parsing the input file
from bs4 import BeautifulSoup
# needed for reg expressions for the find functions in BeautifulSoup4
import re
# needed in order to make requests to ClassieEvals
import requests

with requests.Session() as session:
    # this function will be used as a sign-on to ClassieEvals
    def input_user_info():
        # THIS IS THE PART WHERE WE USE REQUESTS IN ORDER TO ACCESS CLASSIEEVALS
        j = session.get("https://classie-evals.stonybrook.edu/")
        username = input("Enter in your username: ")
        password = input("Enter in your password: ")
        payload = {'j_username': username,
                   'j_password': password,
                   '_eventId_proceed': '',
                   'donotcache': 1}
        k = session.post("https://sso.cc.stonybrook.edu/idp/profile/cas/login?execution=e1s1", data=payload)
        # this starts the part where we bypass DUO, which is the 2 factor authentification system
        a = BeautifulSoup(k.content, 'html.parser')
        b = a.find('iframe')
        tx_attr = b.attrs['data-sig-request'].split(":", -1)[0]
        app = b.attrs['data-sig-request'].split(":", -1)[1]
        parent1 = 'https://sso.cc.stonybrook.edu/idp/profile/cas/login?execution=e1s2'
        parameters = {'tx': tx_attr,
                      'parent': parent1,
                      'v': 2.6}
        k = session.get('https://api-4c3c7a60.duosecurity.com/frame/web/v1/auth', params=parameters)
        a = BeautifulSoup(k.content, 'html.parser')
        b = a.find('form').find_all('input')
        payload2 = {'tx': b[0].attrs['value'],
                    'parent': b[1].attrs['value'],
                    'referer': 'https://sso.cc.stonybrook.edu/',
                    'java_version': b[2].attrs['value'],
                    'flash_version': b[3].attrs['value'],
                    'screen_resolution_width': b[4].attrs['value'],
                    'screen_resolution_height': b[5].attrs['value'],
                    'color_depth': b[6].attrs['value'],
                    'is_cef_browser': b[6].attrs['value'],
                    'is_ipad_os': b[7].attrs['value']}
        k = session.post('https://api-4c3c7a60.duosecurity.com/frame/web/v1/auth', params=parameters, data=payload2)
        a = BeautifulSoup(k.content, 'html.parser')
        b = a.find('input').attrs['value']
        payload1 = {'_eventId': 'proceed',
                    'sig_response': str(b + ':' + app)}
        k = session.post("https://sso.cc.stonybrook.edu/idp/profile/cas/login?execution=e1s2", data=payload1)
        # this marks the end of bypassing the DUO authentification system
        l = session.get("https://classie-evals.stonybrook.edu/")

    # this class will be used to signify a class from ClassieEvals


    class inputClass:
        class_num = None
        season = None
        year = None
        class_properties = {'class_code': None,
                            'time': None,
                            'class_type': None,
                            'class_name': None,
                            'professors': None,
                            'positives': None,
                            'negatives': None}

        times_to_code = {
            'Summer 2020': "1206", 'Spring 2020': "1204", 'Winter 2020': "1201",
            'Fall 2019': "1198", 'Summer 2019': "1196", 'Spring 2019': "1194", 'Winter 2019': "1191",
            'Fall 2018': "1188", 'Summer 2018': "1186", 'Spring 2018': "1184", 'Winter 2018': "1181",
            'Fall 2017': "1178", 'Summer 2017': "1176", 'Spring 2017': "1174", 'Winter 2017': "1171",
            'Fall 2016': "1168", 'Summer 2016': "1166", 'Spring 2016': "1164", 'Winter 2016': "1161",
            'Fall 2015': "1158", 'Summer 2015': "1156", 'Spring 2015': "1154", 'Winter 2015': "1151",
            'Summer 2014': "1146", 'Spring 2014': "1144"}

        def set_input_class_info(self):
            self.class_num = input("Enter in the class # in the EE department you want to search for: ")
            self.season = input("Enter in the season you want to look at: ").title().strip()
            self.year = input("Enter in the year you want to look for: ")

        # these functions will be used to get the important properties of the class
        def get_class_num(self):
            return self.class_num

        def get_class_season(self):
            return self.season

        def get_class_year(self):
            return self.year

        def get_positive_comments(self):
            return self.class_properties['positives']

        def get_negative_comments(self):
            return self.class_properties['negatives']

        def get_class_professors(self):
            return self.class_properties['professors']

        # this function will be used to set the class properties from parsing
        def set_class_info(self):
            time = self.times_to_code[self.season + ' ' + self.year]
            input_classie = {'SearchKeyword': 'ese+' + self.class_num,
                             'SearchTerm': time}

            n = session.get("https://classie-evals.stonybrook.edu/" + "?SearchKeyword="
                            + input_classie['SearchKeyword'] + "&SearchTerm=" + input_classie['SearchTerm'])
            classes_chosen = BeautifulSoup(n.text, 'html.parser').find('tbody').find_all('tr')
            classes_found = [{'code': chosen.contents[1].a.string,
                              'name': chosen.contents[3].string.replace("\r", " ").replace("\n", " ").strip(),
                              'instructor': chosen.contents[5].a.string,
                              'website': chosen.contents[1].a['href']
                              } for chosen in classes_chosen]
            print("Here is what was found:\n")
            print("Class Code #\t\t Class Name \t\t  Class Instructor")
            for classes in classes_found:
                print(classes['code'] + "\t\t" + classes['name'] + "\t\t" + classes['instructor'])
            class_code = input("Enter in a class code you want to use: ")

            for classes in classes_found:
                if classes['code'] == class_code.strip().upper():
                    web_url = "https://classie-evals.stonybrook.edu/" + classes['website']
                    l = session.get(web_url)
                    # END OF ACCESSING THE INTERNET WITH REQUESTS

                    # PARSING OF THE FILE all of this code is for the part where we open up the file and see what are
                    # the possible positives(aka the section What was valuable about this course? on ClassieEvals)
                    # and what are the possible negatives(aka the section What could be improved about this course?
                    # on ClassieEvals)
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

                    self.class_properties = {'class_code': class_description[0],
                                             'time': class_description[1],
                                             'class_type': class_description[2].title(),
                                             'class_name': class_description[3],
                                             'professors': class_description[4].replace(" and ", ", ").split(", ")}
                    print(self.class_properties)

                    # finding the section with the valuable aspects of the course
                    found_pos = j.find('h4', string=re.compile('What was valuable about this course?'))
                    # look for the next section block
                    found_pos = found_pos.find_next('ul')
                    # within the section for the valuable aspects of the code, look for all the <li> tags
                    valuables = found_pos.find_all('li')
                    # store the comments into the positive variable and strip off leading whitespace
                    positives = [valuable.text.strip() for valuable in valuables]
                    self.class_properties['positives'] = positives

                    # finding the section with the needs improvement aspects of the course
                    found_neg = j.find('h4', string=re.compile('What could be improved about this course?'))
                    # finding the next section block
                    found_neg = found_neg.find_next('ul')
                    # within the section for the valuable aspects of the code, look for all the <li> tags
                    needs_improvements = found_neg.find_all('li')
                    # store the comments into the negative variable and strip off leading whitespace
                    negatives = [needs_improvement.text.strip() for needs_improvement in needs_improvements]
                    self.class_properties['negatives'] = negatives
                    break
                    # END OF PARSING OF THE FILE
