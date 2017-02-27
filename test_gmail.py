import smtplib
from email.mime.text import MIMEText
import configure

msg = MIMEText("Hello World!")

me =   configure.EMAIL_ADDRESS
you =  configure.DESTINATION_EMAIL

msg['Subject'] = 'HELLO!'
msg['From'] = me
msg['To'] = you

s = smtplib.SMTP_SSL('smtp.gmail.com:465')
s.login(configure.EMAIL_ADDRESS, configure.EMAIL_PASSWORD)
s.sendmail(me, [you], msg.as_string())
s.quit()
