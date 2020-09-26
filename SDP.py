# needed for parsing the input file
from bs4 import BeautifulSoup
# needed for reg expressions for the find functions in BeautifulSoup4
import re

# all of this code is for the part where we open up the file and see
# what are the possible positives(aka the section What was valuable about this course? on Classie Evals) and
# what are the possible negatives(aka the section What could be improved about this course? on Classie Evals)
with open("ESE118-01.txt", "r") as infile:
    j = BeautifulSoup(infile, 'html.parser')
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

    print(class_description)
    class_properties = {'class_code': class_description[0],
                        'time': class_description[1],
                        'class_type': class_description[2],
                        'class_name': class_description[3],
                        'professors': class_description[4:]}
    print(class_properties)

    # finding the section with the valuable aspects of the course
    found_pos = j.find('h4', string=re.compile('What was valuable about this course?'))
    # look for the next section block
    found_pos = found_pos.findNextSibling("div")
    # within the section for the valuable aspects of the code, look for all the <li> tags
    valuables = found_pos.find_all('li')
    # store the comments into the positive variable and strip off leading whitespace
    positives = [valuable.text.lstrip() for valuable in valuables]

    # finding the section with the needs improvement aspects of the course
    found_neg = j.find('h4', string=re.compile('What could be improved about this course?'))
    # finding the next section block
    found_neg = found_neg.findNextSibling("div")
    # within the section for the valuable aspects of the code, look for all the <li> tags
    needs_improvements = found_neg.find_all('li')
    # store the comments into the negative variable and strip off leading whitespace
    negatives = [needs_improvement.text.lstrip() for needs_improvement in needs_improvements]

    # section for printing everything out for debugging
    print("\n\n")
    print("Here are the comments for what people thought was valuable about the course:")
    for positive in positives:
        print(positive)
    print("\n\n")
    print("Here are the comments for what people thought the course needed improvement:")
    for negative in negatives:
        print(negative)
