import smtplib
import ssl
import os
import pandas as pd
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  # For SSL

# Recipient email addresses
RECIPIENTS = ['pepijnbaggen@gmail.com', 'tlcolsen@hotmail.com','fwillemsen06@gmail.com', 'eline.sebregts@gmail.com', 'danielbreure@hotmail.nl', 'salknopper@gmail.com', 'bischoffcasper@gmail.com', 'francescaborghmans@gmail.com', 'mika.verhulst@icloud.com' ]  # Add other email addresses as needed

# OpenAI API configuration

# Load the CSV file
df = pd.read_csv('rooster.csv', sep=';')

df['Datum'] = pd.to_datetime(df['Datum'], dayfirst=True)
today = pd.to_datetime(datetime.datetime.today())
upcoming_schedules = df[df['Datum'] >= today]

# Sort the DataFrame by date
upcoming_schedules = upcoming_schedules.sort_values(by='Datum')

if upcoming_schedules.empty:
    print("No upcoming schedules found.")
    exit()

next_schedule = upcoming_schedules.iloc[0]

# Extract the date and assignments
schedule_date = next_schedule['Datum'].strftime('%d-%m-%Y')

# Build the task assignments
tasks = next_schedule.drop('Datum')  # Exclude the 'Datum' column

# Generate AI message


# Get weather forecast
def get_weather_forecast(city_name='Leiden'):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&cnt=7&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            print(f"Failed to get weather data: {data.get('message', '')}")
            return ""
        
        forecast = data['list']
        weather_info = "<p><strong>Weekly Weather Forecast:</strong></p><ul>"
        for day in forecast:
            date = datetime.datetime.fromtimestamp(day['dt']).strftime('%A, %d %B %Y')
            temp = day['main']['temp']
            description = day['weather'][0]['description'].capitalize()
            weather_info += f"<li>{date}: {description}, {temp}°C</li>"
        weather_info += "</ul>"
        print(f"Weather info generated: {weather_info}")
        return weather_info
    except Exception as e:
        print(f"Failed to get weather forecast: {e}")
        return ""

weather_info = get_weather_forecast()

# Define the email subject
subject = f'Cleanup Schedule for the Week of {schedule_date}'

# Create the HTML body
body = f"""
<html>
  <body>
    <p><strong>Hey stelletje feuten, hierbij het schoonmaak rooster van deze week! {schedule_date}</strong></p>
<img src="{'https://media.ia.utwente.nl/amelie/activities/icon/Feutens1e2.mp4.gif'}" alt="Weekly Cleanup Schedule GIF" style="width:20%;height:auto;">
    
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
    <p>Doe je taak voor woensdag 18:00 anders boete </p>
  </body>
</html>
"""

# Create the email message
message = MIMEMultipart('alternative')
message['Subject'] = f'Schoonmaak Rooster DKN {schedule_date}'
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
