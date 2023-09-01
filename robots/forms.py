from django.forms import ModelForm
from robots.models import Robot


class RobotForm(ModelForm):
    """
    Форма сделана для удобства валидации встроенными методами Джанго.
    """
    class Meta:
        model = Robot
        fields = ['serial', 'model', 'version', 'created']