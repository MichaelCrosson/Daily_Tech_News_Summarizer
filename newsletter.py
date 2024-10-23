import smtplib
import ssl
import os
import pandas as pd
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime

# Load CSV file with news summaries
news_summaries = pd.read_csv('newssummaries.csv')

# Get the current date
date = datetime.now().strftime("%d-%M-%Y")

# Load environment variables for email credentials
load_dotenv()
gmail_address = os.getenv("GMAIL_ADDRESS")
gmail_password = os.getenv("GMAIL_PASSWORD")

# Create a new email message
email = EmailMessage()
email["Subject"] = f"{date} - Daily Dose of Tech News"
email["From"] = gmail_address

# Build the newsletter HTML content
html_content = '''
<html>
<head></head>
<body>
    <h1>Daily Tech News - {date}</h1>
    <p>Brought to you by <b>Mitch</b></p>
    <hr>
    <ul>
'''.format(date=date)

# Loop through each news item and add it to the HTML content
for index, row in news_summaries.iterrows():
    html_content += f'''
    <li>
        <h3>{row['Title']}</h3>
        <p>{row['Text']}</p>
        <p><a href="{row['Link']}">Read more</a></p>
        <p><i>Source: {row['Origin']}</i></p>
    </li>
    <hr>
    '''

# Close the HTML content
html_content += '''
    </ul>
</body>
</html>
'''

# Add the HTML content to the email
email.add_alternative(html_content, subtype='html')

# List of subscribers
subscriber_email_addresses = ['nossorc2@gmail.com']  # Add more email addresses as needed

# Set up the secure SSL context and send the email
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as smtp_server:
    smtp_server.login(gmail_address, gmail_password)
    
    for subscriber_email in subscriber_email_addresses:
        email["To"] = subscriber_email
        smtp_server.send_message(email)

print("Newsletter sent successfully!")
