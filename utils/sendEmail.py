import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import dotenv

dotenv.load_dotenv()

EMAIL=os.getenv('EMAIL')
PASS=os.getenv('EMAIL_PASSWORD')

def User_mail(email='',status=''):
    server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    server.starttls()
    server.login(EMAIL,PASS)

    msg = MIMEMultipart() 

    message =f'this package status is updated to {status}'

    msg['From']=EMAIL
    msg['To']=email
    msg['Subject']="your order has updated"
    
    msg.attach(MIMEText(message, 'plain'))
    
    server.send_message(msg)
    
    del msg
    server.quit()



def send_html(email='',status=''):

    server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    server.starttls()
    server.login(EMAIL,PASS)

    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Order"
    msg['From'] = EMAIL
    msg['To'] = email

    # Create the body of the message (a plain-text and an HTML version).

    html_pendding = f"""\
        <html>
        <head>
        </head>
        <body>
            <p>Hi your order is been Pending</p>
            <br/>
            <span style="font-size:60px;color:orange;">Pending</span>
            <br/>
            <span style="font-size:60px">In Progress</span>
            <br/>
            <span style="font-size:60px">Delivered</span>
        </body>
        </html>
    """

    html_progress = f"""\
        <html>
        <head>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
        </head>
        <body>
            <p>Hi your order is been In Progress</p>
            <br/>
            <span style="font-size:60px;color:orange;">Pending</span>
            <br/>
            <span style="font-size:60px;color:blue;">In Progress</span>
            <br/>
            <span style="font-size:60px;">Delivered</span>
        </body>
        </html>
    """

    html_finish = f"""\
        <html>
        <head>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
        </head>
        <body>
            <p>Hi your order is been delivered</p>
            </br>
            <span style="font-size:60px;color:orange;">Pending</span>
            </br>
            <span style="font-size:60px;color:blue;">In Progress</span>
            </br>
            <span style="font-size:60px;color:green;">Delivered</span>
        </body>
        </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.

    if status=='Pending':
        part1 = MIMEText(html_pendding, 'html')
        msg.attach(part1)
    if status=='In progress':
        part1 = MIMEText(html_progress, 'html')
        msg.attach(part1)
    if status=='Delivered':
        part1 = MIMEText(html_finish, 'html')
        msg.attach(part1)

    server.send_message(msg)
    del msg

    server.quit()