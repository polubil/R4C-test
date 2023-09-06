import os
from datetime import datetime, timedelta

from django.http import FileResponse
from django.shortcuts import render
from django.views import View

from R4C import settings
from robots.tasks import generate_report


class ReportView(View):
    http_method_names = ['get']
    template_name = 'robots/templates/report.html'

    def get(self, request) -> render:

        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        filename = f"{start_date.strftime('%Y.%m.%d')}-{end_date.strftime('%Y.%m.%d')}.xlsx"
        path_to_file = f"{settings.REPORT_DIR}/{filename}"

        if not os.path.exists(path_to_file):
            generate_report.delay(start_date, end_date)
            return render(
                request,
                template_name=self.template_name,
                context={'filename': None}
            )

        return render(request, template_name=self.template_name, context={'filename': filename})


def download_report(request, filename: str) -> FileResponse:
    # Путь к файлу, название директории с отчетом указывается в settings.py
    path_to_file = os.path.join(settings.REPORT_DIR, filename)
    response = FileResponse(open(path_to_file, 'rb'), as_attachment=True, filename=filename)
    return response
