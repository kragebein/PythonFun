#!/usr/bin/python3
import smtplib
import cgi
from email.message import EmailMessage
from socket import gaierror

class mailer():
    def __init__(self):
        self.smtp = 'mail.trippal.org'
        self.smtp_p = 25
        self.login = True
        self.pw = 'martypewz'
        self.uname = 'Ubz7!=4TZ8Bm'

    def sendmail(self, to, sender, sub, content, altcontent=None):
        if not isinstance(to, list):
            return("TO must be a list!")
        if len(content) == 0:
            return("Content cannot be empty")
        if len(sub) == 0:
            return("Subject cannot be empty")
        if altcontent is None:
            altcontent = "If you cannot read this message, you have a email client that doesnt support html encoded emails. Drag this email into your browser to read the contents."
        
        msg = EmailMessage()
        msg['Subject'] = sub
        msg['From'] = sender
        msg['To'] = sender
        msg['Bcc'] = ', '.join(to)
        msg.set_content("""{}""".format(altcontent))
        msg.add_alternative("""{}""".format(content), subtype='html')
        # save the email to file
        with open('{}.msg'.format(sub), 'wb') as savefile:
            savefile.write(bytes(msg))

        # send it
        try:
            print('Attempting to send mail')
            with smtplib.SMTP(self.smtp, self.smtp_p) as sm:
                if self.login is True:
                    sm.login(self.uname, self.pw)
                sm.send_message(msg)
            print('Sendt.')
        except (gaierror, ConnectionRefusedError):
            print('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to the server. Wrong user/password?')
        except smtplib.SMTPException as e:
            print('SMTP error occurred: ' + str(e))

daim = mailer()
daim.sendmail(['stian.langvann@gmail.com', 'stian@langwater.nl'], 'support@trippal.com', 'Dette er en test', '<br>center>test</center><br>')
