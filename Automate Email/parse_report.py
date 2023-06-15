from re import search
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import imaplib
import email

# Login
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('abc@gmail.com', '***************')
mail.select('inbox')

# Iterate through mail body
typ, search_data = mail.search(None, '(FROM "@noreply.in")' )
for num in search_data[0].split()[-50:-1]:
    typ, data = mail.fetch(num, '(RFC822)')
    email_message = email.message_from_string(data[0][1].decode())
    
    if email_message['subject'] == "Retail Report "+(datetime.now() - timedelta(1)).strftime("%d-%b-%Y"):
        for header in ['subject', 'from', 'date']:
            print('%s: %s' % (header.upper(), email_message[header]))
        for part in email_message.walk():
            if part.get_content_type() == "text/html":
                body = part.get_payload(decode=True)
                print("BODY:\n")
                report = pd.read_html(body)    # Report assigned to dataframe
                print(report)
                print('\n\n')
            else:
                continue

# Logout from session
mail.close()
mail.logout()
