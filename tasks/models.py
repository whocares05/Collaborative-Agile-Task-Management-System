from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.utils import timezone
# Create your models here.

class workspace(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='owned_workspaces')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Label(models.Model):
    name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7, default="#3b82f6") # Hex color code (e.g., Bootstrap primary blue)
    workspace = models.ForeignKey(workspace, on_delete=models.CASCADE, related_name='labels')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'workspace'], name='unique_label_per_workspace')
        ]

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in progress', 'In Progress'),
        ('REVIEW', 'In Review'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    status =models.CharField(max_length=20,choices=STATUS_CHOICES,default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='LOW')

    workspace=models.ForeignKey(workspace,on_delete=models.CASCADE,related_name='tasks')
    assignee=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_tasks')
    collaborators=models.ManyToManyField(User,blank=True,related_name='collaborated_tasks')
    Labels=models.ManyToManyField(Label,blank=True,related_name='tasks')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes=[
            models.Index(fields=['status','priority']),
            models.Index(fields=['due_date']),
        ]

        constraints = [
                models.UniqueConstraint(
                fields=['title', 'workspace'], 
                name='unique_task_title_per_workspace'
            ),
            models.CheckConstraint(
                condition=Q(due_date__gt=F('created_at')) | Q(due_date__isnull=True),
                name='due_date_must_be_after_creation'
            )
        ]

    def __str__(self):
        return f"[{self.status}] {self.title}"