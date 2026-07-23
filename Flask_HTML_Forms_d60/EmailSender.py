'''
    Class for the EmailSender. Responsible for init the smtplib server and sending emails out.
'''

import smtplib

class EmailSender():
    def __init__(self,
                 email: str,
                 password: str,
                 host: str="smtp.gmail.com",
                 port: int=587):
        ''' Init the EmailSender with email, port'''
        self.email = email
        self.password = password
        self.host = host
        self.port = port

    def send_email(self, content: str, from_addr: str, to_addr: str):
        ''' Send an email.'''
        print(content)
        # Send an email to myself as the birthday person
        with smtplib.SMTP(host=self.host, port=self.port) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(
                from_addr=from_addr,
                to_addrs=to_addr,
                msg=f"Subject: Test Email\n\n{content}"
        )