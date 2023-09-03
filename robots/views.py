from django.views import View
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from robots.forms import RobotForm
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class AddRobotView(View):
    http_method_names = ["post"]

    def post(self, request):
        robot = json.loads(request.body)
        robot["serial"] = f'{robot.get("model")}-{robot.get("version")}'  # формируем серийный номер
        # пихаем в форму данные, которые пришли с запросом. Для валидации встроенными методами Django
        robot = RobotForm(robot)
        if robot.is_valid():
            robot.save()
            return JsonResponse(robot.cleaned_data, status=201)
        else:
            return JsonResponse(robot.errors, status=422)
