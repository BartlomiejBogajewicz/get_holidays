import pandas as pd 
import smtplib, ssl
import json 

def send_mail():

    f = open('holidays.json')   

    json_read = json.loads(f.read())

#get max length of each column to properly format the final message

    max_name = len(max([a[0] for a in json_read['data']],key=len)) + 1
    max_date = len(max([a[1] for a in json_read['data']],key=len)) + 1
    max_country = len(max([a[2] for a in json_read['data']],key=len)) + 1

    message = f'{"Name":<{max_name}}' + f'{"Date":<{max_date}}' + f'{"Country":<{max_country}}' + '\n'

    for value in json_read['data']:
        message += f'{value[0]:<{max_name}}' + f'{value[1]:<{max_date}}' + f'{value[2]:<{max_country}}' + '\n'

    f.close()
    
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()


    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("gmail_email", 'password')
        server.sendmail("email_from", "email_to", message)


if __name__ == "__main__":

    send_mail()
