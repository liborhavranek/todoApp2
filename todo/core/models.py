from django.db import models

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    date_planned_completion = models.DateTimeField(blank=True, null=True)
    date_completion = models.DateTimeField(blank=True, null=True)

    
    

