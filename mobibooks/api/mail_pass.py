import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from jinja2 import Environment


toaddress = 'chelluri.abhinav@gmail.com'#'SUPport@mobibooks.com'#chelluri.abhinav@gmail.com"#request.data['merchantemail']

EMAIL_HOST = 'mail.repuzone.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@repuzone.com'
EMAIL_HOST_PASSWORD = 'mobigo@123'

c = open('/home/www/mobibooks/email.html','r')
TEMPLATE = c.read()

msgRoot = MIMEMultipart('related')
msgRoot['From'] = 'noreply@repuzone.com'
msgRoot['To'] = toaddress
msgRoot['Subject'] = 'Forgot Password OTP\n'

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText(Environment().from_string(TEMPLATE).render(name='Abhinav',phone='9999999999',message='message'),"html")

msgAlternative.attach(msgText)

img_data = open('/home/www/mobibooks/repuzone_logo.PNG', 'rb').read()
msgImage = MIMEImage(img_data)

msgImage.add_header('Content-ID', '<image>')
msgRoot.attach(msgImage)

try:
 server = smtplib.SMTP(EMAIL_HOST+':'+str(EMAIL_PORT))
 server.ehlo()
 server.starttls()
 server.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
 server.sendmail(EMAIL_HOST_USER,toaddress,msgRoot.as_string())
 server.quit()
 print('success')
except:
 raise
 print('error')

