import smtplib
import configparser
from email.mime.text import MIMEText


class MailHelper:
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read('../seebug.cfg')
        self.mail_host = cf.get('mail', 'mail_host')
        self.mail_user = cf.get('mail', 'mail_user')
        self.mail_passwd = cf.get('mail', 'mail_passwd')
        self.mail_port = cf.get('mail', 'mail_port')
        self.mail_to_list = cf.get('mail', 'mail_to_list').split(',')

    def send_mail(self, sub, content):
        me = 'Seebug_Spider' + '<' + self.mail_user + '>'
        msg = MIMEText(content)
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ';'.join(self.mail_to_list)
        server = smtplib.SMTP_SSL(self.mail_host, self.mail_port)  # 邮件服务器及端口号
        try:
            server.login(self.mail_user, self.mail_passwd)
            server.sendmail(me, self.mail_to_list, msg.as_string())
            print('发送成功')
            return 1
        except smtplib.SMTPException as e:
            print('发送失败')
            print('错误信息：' + e)
            return -1
        finally:
            server.quit()


if __name__ == '__main__':
    sub = '发送测试'
    content = '发送测试————正文'

    mail_helper = MailHelper()
    mail_helper.send_mail(sub, content)
