from collections import defaultdict
from datetime import datetime

from celery import shared_task
from openpyxl.workbook import Workbook

from R4C import settings


@shared_task(name='generate_report')
def generate_report(start_date: datetime, end_date: datetime) -> None:
    # импортируем тут, так как при импорте в начале файла выпадает эксепшн инициализации приложения Django
    from robots.models import Robot

    robots = Robot.objects.filter(created__gte=start_date)
    print(robots)# получаем всех роботов

    # Создаем таблицу, удаляем первый лист - сделаем всё в цикле.
    wb = Workbook()
    if robots:
        wb.remove(wb['Sheet'])

    versions_count = defaultdict(lambda: defaultdict(int))  # Словарь для хранения количества версий

    for robot in robots:
        versions_count[robot.model][robot.version] += 1  # Увеличиваем счетчик для данной версии

    for model, version_data in versions_count.items():
        ws = wb.create_sheet(title=model)
        ws.append(["Модель", "Версия", "Количество за месяц"])
        for version, count in version_data.items():
            ws.append([model, version, count])

    # обзываем файл и указываем путь для сохранения.
    filename = f"{start_date.strftime('%Y.%m.%d')}-{end_date.strftime('%Y.%m.%d')}.xlsx"
    path_to_file = f"{settings.REPORT_DIR}/{filename}"

    try:
        wb.save(filename=path_to_file)
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
