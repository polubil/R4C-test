from typing import List

from .celery import app
from django.core.mail import BadHeaderError, send_mail


@app.task(bind=True, max_retries=3)
def send_mail_task(self, recipients: List[str], model: str, version: str) -> None:
    subject = "Робот теперь в наличии!"
    from_email = "sales@r4c.com"
    message = (
        "Добрый день!\n"
        f"Недавно вы интересовались нашим роботом модели {model}, версии {version}.\n"
        "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами\n"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipients
        )
    except BadHeaderError as e:
        print(f"Ошибка при отправке письма: {str(e)}")
    except Exception as e:
        print(f"Произошла ошибка при отправке письма: {str(e)}")
        # Повторим эту задачу с задержкой в 60 секунд.
        self.retry(countdown=60)
