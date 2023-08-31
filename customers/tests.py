import json
from unittest.mock import patch

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from customers.tasks import send_mail_task
from orders.models import Order


class RobotSignalTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(email="test_mail_address@example.com")
        self.robot_data_wo_serial = {
            "model": "A1",
            "version": "B1",
            "created": "2023-08-28 21:03:39"
        }
        self.robot_serial = "A1-B1"
        self.order = Order.objects.create(
            customer=self.customer, robot_serial=self.robot_serial
        )

    @patch("customers.tasks.send_mail_task.delay")
    def test_signal_handler_sends_email(self, mock_send_mail_delay):
        url = reverse("new_robot")
        self.client.post(url, data=json.dumps(self.robot_data_wo_serial), content_type="application/json")

        # Проверяем, что таска-заглушка была вызвана.
        mock_send_mail_delay.assert_called_once()

        # Вызываем задачу напрямую.
        send_mail_task([self.customer.email], self.robot_data_wo_serial["model"],
                       self.robot_data_wo_serial["version"])

        # Проверяем, было ли отправлено письмо.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Робот теперь в наличии!")

    @patch("customers.tasks.send_mail_task.delay")
    def test_signal_handler_if_no_orders(self, mock_send_mail_delay):
        url = reverse("new_robot")
        self.robot_data_wo_serial["model"] = "A2"  # изменяем модель на ту, на которую нет заказов.
        self.client.post(url, data=json.dumps(self.robot_data_wo_serial), content_type="application/json")

        # Проверяем, что таска-заглушка не вызывалась.
        mock_send_mail_delay.assert_not_called()

        # Проверяем, что письмо не было отправлено.
        self.assertEqual(len(mail.outbox), 0)


class SendMailTaskTestCase(TestCase):
    def test_send_mail_task(self):
        recipients = ["test_mail_address@example.com"]
        model = "A1"
        version = "B1"

        # Вызываем задачу Celery
        send_mail_task(recipients, model, version)

        # Проверяем, что письмо было отправлено и было отправлено корректно
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Робот теперь в наличии!")
        self.assertIn(f"Недавно вы интересовались нашим роботом модели {model}, версии {version}.", mail.outbox[0].body)
        self.assertIn("Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами",
                      mail.outbox[0].body)

        # Проверяем список получателей
        self.assertEqual(mail.outbox[0].recipients(), recipients)
