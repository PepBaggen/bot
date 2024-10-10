import smtplib
import ssl
import os
import pandas as pd
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
EMAIL_ADDRESS = os.getenv('kalenelbot@gmail.com')  # Your email address
EMAIL_PASSWORD = os.getenv('htix amdk wtvr xihx')  # Your app password
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  # For SSL

# Recipient email addresses
RECIPIENTS = ['pepijnbaggen@gmail.com']  # Replace with actual emails

# Load the CSV file
df = pd.read_csv('rooster.csv')

# Load or initialize the current index
if os.path.exists('current_index.txt'):
    with open('current_index.txt', 'r') as file:
        current_index = int(file.read())
else:
    current_index = 0

# Get the current row
if current_index >= len(df):
    current_index = 0  # Reset to the first row if at the end
row = df.iloc[current_index]

# Create the email content
subject = 'Cleanup Schedule for This Week'
body = f"""
<html>
  <body>
    <p><strong>Cleanup Schedule for This Week</strong></p>
    <p><strong>Task:</strong> {row['Task']}</p>
    <p><strong>Assigned To:</strong> {row['Assigned To']}</p>
  </body>
</html>
"""

# Create the email message
message = MIMEMultipart('alternative')
message['Subject'] = subject
message['From'] = EMAIL_ADDRESS
message['To'] = ', '.join(RECIPIENTS)

# Attach the HTML version
part = MIMEText(body, 'html')
message.attach(part)

# Send the email
context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENTS, message.as_string())
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")

# Update the current index
current_index += 1
with open('current_index.txt', 'w') as file:
    file.write(str(current_index))
