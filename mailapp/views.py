from django.shortcuts import render
from rest_framework import generics
from datetime import date
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Employee, EmailTemplate
from .serializers import EmployeeSerializer, EmailTemplateSerializer
import logging
from django.db import transaction

class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class SendEventEmail(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    logger = logging.getLogger(__name__)
    MAX_EMAIL_RETRIES = 3

    def perform_create(self, serializer):
        employee = serializer.save()

        # Get today's date
        today = date.today()

        # Check for upcoming birthdays
        if today.month == employee.birth_date.month and today.day == employee.birth_date.day:
            self.send_event_email(employee, "Birthday")

        # Check for upcoming work anniversaries (assuming anniversaries are on the same day each year)
        if today.month == employee.work_anniversary.month and today.day == employee.work_anniversary.day:
            self.send_event_email(employee, "Work Anniversary")

    def send_event_email(self, employee, event_type, retries=0):
        try:
            # Get the corresponding email template
            template = EmailTemplate.objects.get(event_type=event_type)

            # Create and send the email
            subject = template.subject
            message = template.message % {'employee_name': employee.name}
            from_email = 'saurabhkurhade18@gmail.com'
            recipient_list = [employee.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        except EmailTemplate.DoesNotExist:
            # Handle the case where no email template is found for the event type
            self.logger.warning(f"No email template found for {event_type} event for employee {employee.name}.")
        except Exception as e:
            # Handle any other exceptions that may occur during email sending
            self.logger.error(f"Failed to send {event_type} email for employee {employee.name}: {str(e)}")

            # Retry sending the email up to the maximum number of retries
            if retries < self.MAX_EMAIL_RETRIES:
                self.logger.info(f"Retrying sending {event_type} email for employee {employee.name}. Retry {retries + 1}/{self.MAX_EMAIL_RETRIES}")
                with transaction.atomic():
                    self.send_event_email(employee, event_type, retries=retries + 1)
            else:
                self.logger.error(f"Maximum retries reached for {event_type} email for employee {employee.name}. Email send failed.")

