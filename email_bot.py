import smtplib
import ssl
import os
import pandas as pd
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # Retrieve your email address from environment variables
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Retrieve your app password from environment variables
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  # For SSL

# Recipient email addresses
RECIPIENTS = ['pepijnbaggen@gmail.com']  # Add other email addresses as needed

# Load the CSV file
df = pd.read_csv('rooster.csv')

# Parse the 'Datum' column as dates
df['Datum'] = pd.to_datetime(df['Datum'], format='%d-%m-%Y')

# Sort the DataFrame by date
df = df.sort_values('Datum')

# Get today's date
today = datetime.datetime.now().date()

# Find the next scheduled date (the closest date on or after today)
upcoming_schedules = df[df['Datum'] >= today]

if upcoming_schedules.empty:
    print("No upcoming schedules found.")
    exit()

next_schedule = upcoming_schedules.iloc[0]

# Extract the date and assignments
schedule_date = next_schedule['Datum'].strftime('%d-%m-%Y')

# Prepare the email content
subject = f'Cleanup Schedule for the Week of {schedule_date}'

# Build the task assignments
tasks = next_schedule.drop('Datum')  # Exclude the 'Datum' column

# Create the HTML body
body = f"""
<html>
  <body>
    <p><strong>Cleanup Schedule for the Week of {schedule_date}</strong></p>
    <table border="1" cellpadding="5" cellspacing="0">
      <tr>
        <th>Task</th>
        <th>Assigned To</th>
      </tr>
"""

# Add each task and assigned person to the email body
for task_name, assigned_to in tasks.items():
    body += f"""
      <tr>
        <td>{task_name}</td>
        <td>{assigned_to}</td>
      </tr>
    """

body += """
    </table>
    <p>Please complete your assigned tasks by the end of the week.</p>
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
