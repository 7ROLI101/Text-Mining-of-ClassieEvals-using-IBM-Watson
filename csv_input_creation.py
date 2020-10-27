import scrape_parse as sp
import csv

sp.input_user_info()
surveyClass = sp.inputClass()
surveyClass.set_input_class_info()
surveyClass.set_class_info()
with open('comments.csv',mode='w',newline='') as file:
    csvwriter = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(surveyClass.get_positive_comments())
    csvwriter.writerow(surveyClass.get_negative_comments())
