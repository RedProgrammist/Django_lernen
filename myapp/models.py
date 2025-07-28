from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='task')
    status = models.CharField(choices=STATUS_CHOICES)
    deadline= models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('title', 'created_at')

    def __str__(self):
        return f"{self.title} ({self.created_at})"

class SubTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(choices=Task.STATUS_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
