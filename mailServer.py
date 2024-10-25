from aiosmtpd.controller import Controller

class CustomMessageHandler:
    async def handle_DATA(self, server, session, envelope):
        print("Получено сообщение от:", envelope.mail_from)
        print("Получатели:", envelope.rcpt_tos)
        print("Содержание:")
        print(envelope.content.decode('utf8', errors='replace'))
        print("Конец сообщения\n")
        return '250 OK'

# Запуск контроллера
controller = Controller(CustomMessageHandler(), hostname='localhost', port=1025)
controller.start()

print("SMTP-сервер запущен на localhost:1025")

# Чтобы сервер продолжал работать, пока не будет прерван
try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    controller.stop()
