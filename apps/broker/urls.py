from django.urls import path

from apps.broker.views.broker_account_view import CreateBrokerAccountView
from apps.broker.views.signals_parse_view import ReceiveSignalAPIView

# <<--------------------------------- Broker URLs --------------------------------->>
urlpatterns = [
    path("accounts/", CreateBrokerAccountView.as_view(), name="create"),
    path("webhook/receive-signal/", ReceiveSignalAPIView.as_view(), name="signals"),
]
