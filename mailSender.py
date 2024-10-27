import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from multipledispatch import dispatch

class MailSender():
    # Настройки отправителя и получателя
    sender_email = "safonovila7@gmail.com"
    receiver_email = "safonovila7@gmail.com"
    receiver_list = []
    app_password = ""

    def __init__(self, sender_address: str):
        self.sender_email = sender_address
        self.message = MIMEMultipart()

    def set_sender(self, sender_address: str):
        self.sender_email = sender_address

    def set_account_password(self, password: str):
        self.app_password = password

    def send_email(self):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email,
                                self.receiver_email,
                                self.message.as_string())
            print("Письмо успешно отправлено.")
        except Exception as e:
            print(f"Ошибка: {e}")

    @dispatch(list)
    def send_email_tolist(self, reciever_list: list):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.app_password)
                for reciever in reciever_list:
                    server.sendmail(self.sender_email,
                                    reciever,
                                    self.message.as_string())
            print("Письма успешно отправлены.")
        except Exception as e:
            print(f"Ошибка: {e}")

    @dispatch()
    def send_email_tolist(self):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.app_password)
                for reciever in self.receiver_list:
                    server.sendmail(self.sender_email,
                                    reciever,
                                    self.message.as_string())
            print("Письма успешно отправлены.")
        except Exception as e:
            print(f"Ошибка: {e}")

    @dispatch(str, str)
    def create_message(self, subject: str, body: str) -> MIMEMultipart:
        # Записывет сообщение в свой объект и возвращает его же
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = subject
        self.message.attach(MIMEText(body, "plain"))
        return self.message

    @dispatch(list)
    def create_message(self, contents: list) -> MIMEMultipart:
        # Записывет сообщение в свой объект и возвращает его же
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = contents[0]
        self.message.attach(MIMEText(contents[1], "plain"))
        return self.message

    def add_reciever(self, new_receiver_address: str):
        if not new_receiver_address: return
        if new_receiver_address in self.receiver_list:
            print(f'{new_receiver_address} is in list already')
            return

        self.receiver_list.append(new_receiver_address)

    def del_reciever(self, receiver_address: str):
        if not receiver_address: return
        if receiver_address not in self.receiver_list:
            print(f'{receiver_address} is not in list already')
            return
        self.receiver_list.remove(receiver_address)





