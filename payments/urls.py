from django.urls import path
from payments.views import *

app_name = "payments"

urlpatterns = [
    path("", payment_dashboard, name="dashboard"),
    path("<int:dispute_id>/pay/", payment_initiate, name="initiate"),
    path("<int:pk>/status/", payment_status, name="status"),
    path("<int:pk>/refund/", refund_request, name="refund"),
    path("refunds/", refunds_admin, name="refunds_admin"),
    path("history/", transaction_history, name="history"),
    path("subscriptions/", subscriptions_list, name="subscriptions"),
    path("invoices/", invoices_list, name="invoices"),
]
