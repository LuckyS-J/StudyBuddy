from django.db import models
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime

# Create your models here.

# TODO 1 Add profile model (profile_picture etc)
# TODO 4 REST API

class Goal(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Done', 'Done'),
    ]

    user = models.ForeignKey(User, related_name='goals',
                             null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='Untitled Goal')
    description = models.TextField(max_length=500)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='New')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)

    def clean(self):
        super().clean()
        if self.deadline and self.deadline < timezone.now().date():
            raise ValidationError("Deadline cannot be in the past.")

    def __str__(self):
        return self.title


class Task(models.Model):
    goal = models.ForeignKey(Goal, related_name='tasks',
                             null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='Untitled Task')
    description = models.TextField(max_length=500)
    is_done = models.BooleanField(default=False)
    created_at = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.title


class Note(models.Model):
    goal = models.ForeignKey(Goal, related_name='notes',
                             null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.text
