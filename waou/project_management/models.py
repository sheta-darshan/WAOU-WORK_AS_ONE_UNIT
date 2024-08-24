from django.db import models
from waou_core.models import UserProfile

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    team = models.ManyToManyField(UserProfile, related_name='projects')
    
    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=50, choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')], default='todo')
    due_date = models.DateField()
    
    def __str__(self):
        return self.name
