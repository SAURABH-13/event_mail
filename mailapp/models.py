from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    birth_date = models.DateField()
    work_anniversary = models.DateField()

    def __str__(self):
        return self.name

class EmailTemplate(models.Model):
    event_type = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.event_type
