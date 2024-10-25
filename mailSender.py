import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "test@example.com"
receiver_email = "receiver@example.com"
subject = "This message was sent as test"
body = "Test body of the message will be here"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

with smtplib.SMTP("localhost", 1025) as server:
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Тестовое письмо отправлено.")
