import smtplib
import ssl
from dotenv import load_dotenv
import os
import pandas as pd
from email.message import EmailMessage
from datetime import datetime

# Get the Gmail credentials from GitHub Secrets (environment variables)
load_dotenv()
gmail_address = os.getenv("GMAIL_ADDRESS")
gmail_password = os.getenv("GMAIL_PASSWORD")

# Ensure that the credentials are loaded properly
assert gmail_address, "GMAIL_ADDRESS environment secret not loaded"
assert gmail_password, "GMAIL_PASSWORD environment secret not loaded"

# Load CSV file with news summaries
news_summaries = pd.read_csv('newssummaries.csv')

# Get the current date
date = datetime.now().strftime("%d-%m-%Y")

# List of subscribers
subscriber_email_addresses = ['nossorc2@gmail.com']  # Add more email addresses as needed

# Build the newsletter HTML content
html_content = f'''
<html>
<head></head>
<body>
    <h1>Daily Tech News - {date}</h1>
    <p>Brought to you by <b>Mitch</b></p>
    <hr>
    <ul>
'''

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

# Set up the secure SSL context
context = ssl.create_default_context()

# Function to send email
def send_email(to_address, content):
    try:
        # Create a new email message for each recipient
        email = EmailMessage()
        email["Subject"] = f"{date} - Daily Dose of Tech News"
        email["From"] = gmail_address
        email["To"] = to_address

        # Add the HTML content to the email
        email.add_alternative(content, subtype='html')

        # Send the email
        smtp_server.send_message(email)
        print(f"Newsletter sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email to {to_address}: {e}")

# Send the email to each subscriber
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp_server:
        # Attempt to login with the provided credentials
        try:
            smtp_server.login(gmail_address, gmail_password)
            print("Login successful.")
        except smtplib.SMTPAuthenticationError as auth_error:
            print(f"SMTP Authentication error: {auth_error}")
            exit(1)
        except Exception as login_error:
            print(f"Login failed: {login_error}")
            exit(1)

        # Send emails to each subscriber
        for subscriber_email in subscriber_email_addresses:
            send_email(subscriber_email, html_content)
except Exception as e:
    print(f"An error occurred: {e}")

# print(html_content)
print("Newsletter sending process completed.")
