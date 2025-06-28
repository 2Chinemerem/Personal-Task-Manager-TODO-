from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=256)
    description= models.TextField(blank=True)
    created_at= models.DateTimeField(default=timezone.now)
    due_date= models.DateField(blank=True, null=True)
    completed= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({'Done' if self.completed else 'pending'} by {self.user})"
    
    def get_absolute_url(self):
        return reverse("task:detail", args=[str(self.id)])
