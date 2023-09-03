import json

from django.test import TestCase
from django.urls import reverse

from robots.models import Robot


class AddRobotViewTestCase(TestCase):
    def setUp(self):
        self.robot_data = {
            "model": "A1",
            "version": "B1",
            "created": "2023-08-28 21:03:39"
        }

    def test_add_robot_view_valid_data(self):
        url = reverse("new_robot")
        response = self.client.post(url, data=json.dumps(self.robot_data), content_type="application/json")

        # Проверяем код статуса ответа
        self.assertEqual(response.status_code, 201)

        # Проверяем, что робот был создан
        self.assertEqual(Robot.objects.count(), 1)

    def test_add_robot_view_invalid_data(self):
        url = reverse("new_robot")
        self.robot_data["model"] = ""  # убираем модель, хотя она обязательна.
        response = self.client.post(url, data=json.dumps(self.robot_data), content_type="application/json")

        # Проверяем код статуса ответа
        self.assertEqual(response.status_code, 422)

        # Проверяем, что робот не был создан
        self.assertEqual(Robot.objects.count(), 0)
