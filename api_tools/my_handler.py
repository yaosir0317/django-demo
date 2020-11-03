import os
import traceback
import json
from datetime import datetime
from logging import Handler
from threading import Thread
from django.core.mail import send_mail
from django.conf import settings
import requests


def postpone(function):
    def postpone_decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return postpone_decorator


class SendEmailHandler(Handler):
    """
    An exception log handler that emails log entries to settings.EXCEPTION_MAIL_LIST.
    """
    active_count = 0

    @postpone
    def send_admin_mail(self, subject, message, mail_from, mail_to, fail_silently):
        if SendEmailHandler.active_count < 5:
            SendEmailHandler.active_count += 1
            send_mail(subject, message, mail_from, mail_to, fail_silently=fail_silently)
            SendEmailHandler.active_count -= 1
        else:
            pass

    def emit(self, record):
        if os.getenv('DONT_SEND_EXCEPTION_MAIL'):  # 应用于本地开发
            return

        # 自定标题
        subject = '%s: %s %s' % (
            'Exception',
            record.levelname,
            record.getMessage()
        )

        def format_subject(subject_info):
            """
            Escape CR and LF characters.
            """
            return subject_info.replace('\n', ' ').replace('\r', ' ')

        subject = format_subject(subject)  # 邮件标题
        message = record.getMessage() + '\n' + traceback.format_exc()

        self.send_admin_mail(subject, message, settings.EXCEPTION_MAIL_FROM, settings.EXCEPTION_MAIL_LIST, False)


class SendFeiShuHandler(Handler):
    """
    An exception log handler that send feishu post.
    """
    active_count = 0

    @postpone
    def send_exceptions(self, title, content):
        txt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "\r\n" + content
        requests.post(url=settings.FEI_SHU_URL, data=json.dumps({
            "title": title,
            "text": txt
        }))

    def emit(self, record):
        # 自定标题
        subject = '%s: %s %s' % (
            'Exception',
            record.levelname,
            record.getMessage()
        )

        def format_subject(subject_info):
            """
            Escape CR and LF characters.
            """
            return subject_info.replace('\n', ' ').replace('\r', ' ')

        subject = format_subject(subject)  # 邮件标题
        # sourceInfo是放于extra的信息
        extra_info = getattr(record, "sourceInfo") if hasattr(record, "sourceInfo") else ""
        message = record.getMessage() + '\n' + traceback.format_exc() + "\n" + extra_info
        self.send_exceptions(subject, message)
