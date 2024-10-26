import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class mailSender():
    # Настройки отправителя и получателя
    sender_email = "safonovila7@gmail.com"
    receiver_email = "safonovila7@gmail.com"
    app_password = ""

    def __init__(self,sender_address:str,reciever_address:str):
        self.sender_email = sender_address
        self.receiver_email = reciever_address
        self.message = MIMEMultipart()

    def set_sender_reciever(self,sender_address:str,reciever_address:str):
        self.sender_email = sender_address
        self.receiver_email = reciever_address

    def set_account_password(self,password:str):
        self.app_password = password

    def send_email(self):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, self.receiver_email, self.message.as_string())
            print("Письмо успешно отправлено.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def create_message(self,subject:str,body:str) -> MIMEMultipart :
        # Записывет сообщение в свой объект и возвращает его же
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = subject
        self.message.attach(MIMEText(body, "plain"))
        return self.message

ms = mailSender("safonovila7@gmail.com","safonovila7@gmail.com")
ms.create_message("Субъект","Суть сообщения тут")
ms.set_account_password(os.getenv('EMAIL_PASS'))
ms.send_email()