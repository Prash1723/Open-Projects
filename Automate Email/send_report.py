from smtplib import SMTP, ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from pretty_html_table import build_table  

#Report Table Builder
subject = "Report"                  ## Subject
shops = "Today's items onboarded"   ## Email body
sender_email = "abc@gmail.com"      ## Sender
receiver_email = "xyz@gmail.com"    ## Receiver
password = "*************"          ## Password
report =                            ## Assign table here

# Assign message body
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["body"] = shops

# Assign report to body
body = build_table(report, 'blue_light')    ## Build a brilliant table using build_table command

# Add email body
message.attach(MIMEText(shops, "plain"))
message.attach(MIMEText(body, "html"))
msg_body = message.as_string()

port = 465 # For SSL
smtp_server = "smtp.gmail.com"

# Create secure email server
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg_body)
    server.quit()

