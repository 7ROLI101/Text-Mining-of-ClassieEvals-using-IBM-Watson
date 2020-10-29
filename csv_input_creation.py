import scrape_parse as sp
import csv

sp.input_user_info()
surveyClass = sp.inputClass()
surveyClass.set_input_class_info()
surveyClass.set_class_info()
with open('comments.csv',mode='w',newline='') as file:
    csvwriter = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
    positives = ['Valuable']
    negatives = ['Needs Improvement']
    csvwriter.writerow(['TYPE','COMMENT'])
    for comment in surveyClass.get_positive_comments():
        positives.append(comment)
        csvwriter.writerow(positives)
        del positives[1]

    for comment in surveyClass.get_negative_comments():
        negatives.append(comment)
        csvwriter.writerow(negatives)
        del negatives[1]
