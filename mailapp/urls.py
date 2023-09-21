from django.urls import path
from .views import EmployeeList, SendEventEmail

urlpatterns = [
    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('send-event-email/', SendEventEmail.as_view(), name='send-event-email'),
]
