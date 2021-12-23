import smtplib



import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения

from email.mime.multipart import MIMEMultipart



def send_email(addr_to, msg_subj, msg_text, files):
    addr_from = "face.comparator@gmail.com"
    password = "miptproject"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = msg_subj

    body = msg_text
    msg.attach(MIMEText(body, 'plain'))

    process_attachement(msg, files)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Создаем объект SMTP
    # server.starttls()                                      # Начинаем шифрованный обмен по TLS
    # server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()


def process_attachement(msg, files):
    for f in files:
        ctype, encoding = mimetypes.guess_type(str(f))
        maintype, subtype = ctype.split('/', 1)
        file = MIMEImage(f.read(), _subtype=subtype)
        file.add_header('Content-Disposition', 'attachment', filename=str(f))
        msg.attach(file)
