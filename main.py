import requests as r
import sendgrid
from sendgrid.helpers.mail import *
import os
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler


logging.basicConfig(    
                        encoding='utf-8', 
                        level=logging.INFO, 
                        format='%(asctime)s %(levelname)s %(message)s', 
                        handlers=[TimedRotatingFileHandler("app.log", when="M", interval=3, backupCount=3)]
                    )

def send_mail(old_ip, new_ip):
    load_dotenv()
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(os.environ.get("EMAIL_FROM"))
    to_email = To(os.environ.get("EMAIL_TO"))
    subject = "Your public IP has changed"
    content = Content("text/plain", "Old IP : " + old_ip + "\nNew IP : " + new_ip)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

providers = ["icanhazip.com", "ifconfig.me", "ipecho.net/plain"]
stored_ip = "./ip.log"

try:
    logging.info("starting process")
    for provider in providers:
        logging.info("connecting to " + provider)
        response = r.get("https://" + provider)
        if response.status_code == 200:
            request_ip = response.content.decode().rstrip()

            if not os.path.exists(stored_ip):
                file = open(stored_ip, 'w+')
                file_ip = ""
            else:
                with open(stored_ip, "r") as fr:
                    file_ip = fr.read()
            if request_ip != file_ip:
                logging.info("ip has changed :")
                logging.info(" -> old ip : " + file_ip)
                logging.info(" -> new ip : " + request_ip)
                logging.info("writing new ip to permanent storage")
                with open(stored_ip, "w") as fw:
                    fw.write(request_ip)
                logging.info("sending email alert")
                send_mail(file_ip, request_ip)

            else:
                logging.info("ip has not changed : " + request_ip)
            logging.info("ending process")
            break
        else:
            logging.warn("skipping " + provider + "because of HTTP return code" + response.status_code)
            
except Exception as e:
    logging.error("Error: %s" % str(e))