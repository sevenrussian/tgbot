import smtplib as smtp
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from config import bot_email, bot_email_password
import mimetypes


async def send_letter(to_email, reply_address, subject, message):
    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'plain'))
    server = smtp.SMTP_SSL('mail.nic.ru:465')
    server.login(bot_email, bot_email_password)
    msg.add_header('reply-to', reply_address)
    msg['subject'] = subject
    server.sendmail(bot_email, to_email, msg.as_string())
    server.quit()


async def send_letter_with_attachment(to_email, reply_address, subject, message, file, filename):
    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'plain'))
    server = smtp.SMTP_SSL('mail.nic.ru:465')
    server.login(bot_email, bot_email_password)
    msg.add_header('reply-to', reply_address)
    msg['subject'] = subject

    attach_file(msg, file, filename)

    server.sendmail(bot_email, to_email, msg.as_string())
    server.quit()


def attach_file(msg, filepath, fname):
    ctype, encoding = mimetypes.guess_type(filepath)
    maintype, subtype = ctype.split('/', 1)
    with open(filepath, 'rb') as fp:
        file = MIMEBase(maintype, subtype)
        file.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=fname)
    msg.attach(file)
