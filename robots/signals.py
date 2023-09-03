from django.dispatch import receiver
from robots.models import Robot
from orders.models import Order
from django.db.models.signals import post_save
from customers.tasks import send_mail_task


@receiver(post_save, sender=Robot)
def make_email_task(sender: Robot, instance: Robot, **kwargs):
    serial = instance.serial
    orders = Order.objects.filter(robot_serial=serial).all()

    if not orders.exists():
        return

    mailboxes = list(orders.values_list("customer__email", flat=True).distinct())
    send_mail_task.delay(mailboxes, instance.model, instance.version)
