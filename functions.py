import smtplib, ssl
from flask import request, jsonify
from textblob import TextBlob


def find_replicate(all):
    random_list = []
    frequency = {}
    for i in range(0, len(all)):
        random_list.append(all[i]["ip"])

    # iterating over the list
    for item in random_list:
        # checking the element in dictionary
        if item in frequency:
            # incrementing the counr
            frequency[item] += 1
        else:
            # initializing the count
            frequency[item] = 1
    return frequency


def mail_admin():
    mail_id = "venkateshprasad310@gmail.com"
    s = smtplib.SMTP('smtp.gmail.com', 587)
    sender = "venkypubg310@gmail.com"
    receiver = mail_id

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("venkypubg310@gmail.com", "Venkatesh*10")

    # message to be sent

    message = f"""Hi Admin,Spam messages detected in your comments section 
    pls go to admin menu for further operations"""
    s.sendmail("venkypubg310@gmail.com", mail_id, message)

    # terminating the session
    s.quit()

    return 1


def sentiment(all, ip):
    y = []
    frequency={}
    for i in range(0, len(all)):
        if all[i]["ip"] == ip:
            y.append(all[i]["comments"])
    lis = []
    for i in range(0, len(y)):

        edu = TextBlob(y[i])
        x = edu.sentiment.polarity
        if x < 0:
            lis.append("negative")

        elif x == 0:
            lis.append("neutral")

        elif x > 0:
            lis.append("positive")

    for item in lis:
        # checking the element in dictionary
        if item in frequency:
            # incrementing the counr
            frequency[item] += 1
        else:
            # initializing the count
            frequency[item] = 1
    print(lis)
    return frequency
