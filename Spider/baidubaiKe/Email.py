from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


class Email(object):
    def __init__(self):
        # 发件人地址
        self.__from_addr = '1084552910@qq.com'
        # 邮箱授权密码
        self.__password = 'uczouzleuhvwbadg'
        # 收件人地址
        self.__to_addr = '1045612428@qq.com'
        # 邮箱服务器地址
        self.__smtp_server = 'smtp.qq.com'

    def _format_addr(self, s):
        """
        格式化邮件地址
        :param s: 输入的地址
        :return: 格式化后的地址
        """
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def eamil(self, n):
        """
        发送邮件
        :param n: 状态码
        :return:
        """
        if n == 0:
            # 设置邮件信息
            msg = MIMEText('Python爬虫运行异常，异常信息为遇到HTTP 403', 'plain', 'utf-8')
            msg['From'] = self._format_addr('Python爬虫一号<%s>' % self.__from_addr)
            msg['To'] = self._format_addr('管理员<%s>' % self.__to_addr)
            msg['Subject'] = Header('一号爬虫运行异常.', 'utf-8').encode()
        else:
            # 设置邮件信息
            msg = MIMEText('任务已完成，请前去查看！', 'plain', 'utf-8')
            msg['From'] = self._format_addr('wcjb<%s>' % self.__from_addr)
            msg['To'] = self._format_addr('master<%s>' % self.__to_addr)
            msg['Subject'] = Header('提示信息.', 'utf-8').encode()
        # 发送邮件
        # SMTP协议默认端口是25
        server = smtplib.SMTP_SSL(self.__smtp_server, 465)
        # 打印出和SMTP服务器交互的所有信息，SMTP协议就是简单的文本命令和响应
        # server.set_debuglevel(1)
        # 方法用来登录SMTP服务器
        server.login(self.__from_addr, self.__password)
        # sendmail()方法就是发邮件，由于可以一次发给多个人，
        # 所以传入一个list，邮件正文是一个str，as_string()
        # 把MIMEText对象变成str。
        server.sendmail(self.__from_addr, self.__to_addr, msg.as_string())
        server.quit()

