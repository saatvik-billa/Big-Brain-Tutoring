import csv
import smtplib
import json

emails_list = []
zoom_link = ''

# ---- GET FILE NAME ----

type = input('Computer Science Lessons or Webinar? ')

def getFileName(type):
    if (''.join(type.split(' ')).lower().find('computerscience') != -1):
        return 'compSci'
    elif (type.lower() == 'webinar'):
        return 'webinar'
    else:
        raise TypeError("Input doesn't match 'computer science' or 'webinar' ")

fileName = getFileName(type);

# ---- READ DATA FROM CSV FILE ----

with open(f'{fileName}.csv', 'rt') as f:
    csv_reader = csv.reader(f)

    next(csv_reader)

    if (fileName == 'webinar'):
        for line in csv_reader:
            if (line[14] != 'true'):
                emails_list.append(line[5])
        zoom_link = line[12].split(' ')[2]
    elif (fileName == 'compSci'):
        for line in csv_reader:
            if (line[4] != 'true'):
                emails_list.append(line[3])


# ---- SEND EMAILS TO ATTENDEES ----

with open("config.json") as json_data_file:
    data = json.load(json_data_file) # get credentials from config file

smtp_object = smtplib.SMTP('smtp.gmail.com', 587) # 587 refers to startTLS connection, 465 is SSL/TLS

# ehlo method will greet the server and establish the connection -- needs to be done immediately after creating smtp obj
smtp_object.ehlo()

smtp_object.starttls() # enables TLS encryption

email = data['email']
password = data['appPassword']

smtp_object.login(email, password)

from_address = email
to_address = emails_list
subject = '' # add subject here
message = '' # add email content here
msg = 'Subject: '+subject+'\n'+message

smtp_object.sendmail(from_address, to_address, msg)

smtp_object.quit()

