import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io
from typing import List

from imageio import imsave

from email.mime.multipart import MIMEMultipart

import numpy as np


def send_email(addr_to: str, msg_subj: str, msg_text: str, files: List) -> None:
    addr_from = "face.comparator@gmail.com"
    password = "miptproject"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = msg_subj

    body = msg_text
    msg.attach(MIMEText(body, 'plain'))

    _process_attachement(msg, files)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.starttls()
    # server.set_debuglevel(True)
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()


def _process_attachement(msg, files):
    for img, name in files:
        img_np = np.array(img).astype(np.uint8)
        fmem = io.BytesIO()
        imsave(fmem, img_np, 'png')
        fmem.seek(0)
        file = MIMEImage(fmem.read(), _subtype=False)
        encoders.encode_base64(file)
        file.add_header('Content-Disposition', 'attachment', filename=name)
        msg.attach(file)
