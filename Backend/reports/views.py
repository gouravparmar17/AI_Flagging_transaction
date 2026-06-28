import csv
from io import BytesIO, StringIO

from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from rest_framework.views import APIView

from fraud_detection.models import FraudPrediction
from transactions.models import Transaction


def _filtered_transactions(user, request):
    qs = Transaction.objects.filter(user=user)
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    if start_date:
        qs = qs.filter(timestamp__date__gte=start_date)
    if end_date:
        qs = qs.filter(timestamp__date__lte=end_date)
    return qs


class CSVReportView(APIView):
    def get(self, request):
        transactions = _filtered_transactions(request.user, request)
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["transaction_id", "amount", "merchant", "location", "type", "timestamp"])
        for txn in transactions:
            writer.writerow([txn.transaction_id, txn.amount, txn.merchant, txn.location, txn.transaction_type, txn.timestamp])

        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="fraud_report.csv"'
        return response


class ExcelReportView(APIView):
    def get(self, request):
        transactions = _filtered_transactions(request.user, request)
        wb = Workbook()
        ws = wb.active
        ws.title = "Transactions"
        ws.append(["Transaction ID", "Amount", "Merchant", "Location", "Type", "Timestamp"])
        for txn in transactions:
            ws.append([txn.transaction_id, float(txn.amount), txn.merchant, txn.location, txn.transaction_type, str(txn.timestamp)])

        stream = BytesIO()
        wb.save(stream)
        response = HttpResponse(
            stream.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="fraud_report.xlsx"'
        return response


class PDFReportView(APIView):
    def get(self, request):
        transactions = _filtered_transactions(request.user, request)
        total = transactions.count()
        fraud_count = FraudPrediction.objects.filter(user=request.user, prediction="Fraud", transaction__in=transactions).count()

        stream = BytesIO()
        p = canvas.Canvas(stream)
        y = 800
        p.drawString(50, y, "Suspicious Transaction Detection Report")
        y -= 25
        p.drawString(50, y, f"Total Transactions: {total}")
        y -= 18
        p.drawString(50, y, f"Fraud Predictions: {fraud_count}")
        y -= 28

        p.drawString(50, y, "Transaction History")
        y -= 20
        for txn in transactions[:25]:
            p.drawString(50, y, f"{txn.transaction_id} | {txn.amount} | {txn.merchant} | {txn.location}")
            y -= 14
            if y < 70:
                p.showPage()
                y = 800

        p.showPage()
        p.save()

        response = HttpResponse(stream.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="fraud_report.pdf"'
        return response
