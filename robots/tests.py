from django.test import TestCase, Client
from django.urls import reverse
import json

# сет с данными которые соответствуют модели.
test_set_ok = {
    "D2", "E3", "G7", "39", "PP", "Жж", "<>", ">>"
}

# сет с данными которые не соответствуют модели.
test_set_err = {
    "...", "DWNAI", "282w", " ", "", "Добрый день", "|\\|"
}


class AddRobotViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('new')

    #  данные полные и соответствуют полям модели.
    def test_valid_robot_creation(self):
        for i in test_set_ok:
            with self.subTest(sequence=test_set_ok):
                data = {
                    "model": i,
                    "version": i,
                    "created": "2022-12-31 23:59:59"
                }
                response = self.client.post(self.url, json.dumps(data), content_type="application/json")
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json()["serial"], f"{i}-{i}")

    #  данные неполные или не соответствуют полям модели
    def test_invalid_robot_creation(self):
        #  Данные заведомо не соответствуют полям модели.
        for i in test_set_err:
            with self.subTest(sequence=test_set_err):
                data = {
                    "model": i,
                    "version": i,
                    "created": "2022-12-31 23:59:59"
                }
                response = self.client.post(self.url, json.dumps(data), content_type="application/json")
                self.assertEqual(response.status_code, 422)

        #  Отсутствует версия, остальные данные корректны.
        for i in test_set_ok:
            with self.subTest(sequence=test_set_err):
                data = {
                    "model": i,
                    "created": "2022-12-31 23:59:59"
                }
                response = self.client.post(self.url, json.dumps(data), content_type="application/json")
                self.assertEqual(response.status_code, 422)

        #  Отсутствует дата, остальные данные корректны.
        for i in test_set_ok:
            with self.subTest(sequence=test_set_err):
                data = {
                    "model": i,
                    "version": i,
                }
                response = self.client.post(self.url, json.dumps(data), content_type="application/json")
                self.assertEqual(response.status_code, 422)

        #  Отсутствует дата и модель, остальные данные корректны.
        for i in test_set_ok:
            with self.subTest(sequence=test_set_err):
                data = {
                    "version": i,
                }
                response = self.client.post(self.url, json.dumps(data), content_type="application/json")
                self.assertEqual(response.status_code, 422)

    #  GET-запрос не разрешен на этом эндпоинте.
    def test_get_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
