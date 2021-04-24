import scrape_parse as sp
import csv

sp.input_user_info()
while True:
    surveyClass = sp.inputClass()
    surveyClass.set_input_class_info()
    surveyClass.set_class_info()
    class_name = surveyClass.get_class_code()
    class_time = str(surveyClass.get_class_season()).upper() + str(surveyClass.get_class_year())
    with open(str(class_name.upper()) + "_" + class_time + '.csv', mode='w', newline='',encoding='utf-8') as file:
        csvwriter = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
        positives = ['Valuable']
        negatives = ['Needs Improvement']
        csvwriter.writerow(['TYPE', 'COMMENT'])
        for comment in surveyClass.get_positive_comments():
            positives.append(comment)
            csvwriter.writerow(positives)
            del positives[1]

        for comment in surveyClass.get_negative_comments():
            negatives.append(comment)
            csvwriter.writerow(negatives)
            del negatives[1]
