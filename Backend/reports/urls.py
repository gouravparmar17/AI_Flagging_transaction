from django.urls import path

from .views import CSVReportView, ExcelReportView, PDFReportView

urlpatterns = [
    path("pdf/", PDFReportView.as_view(), name="report_pdf"),
    path("excel/", ExcelReportView.as_view(), name="report_excel"),
    path("csv/", CSVReportView.as_view(), name="report_csv"),
]
