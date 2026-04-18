from django.urls import path
from .views import ReportCreateView, ReasonChoicesView

urlpatterns = [
    path('create/', ReportCreateView.as_view(), name='create-report'),
    path('reasons/', ReasonChoicesView.as_view(), name='reason-choices'),
]
