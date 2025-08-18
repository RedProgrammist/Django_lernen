from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    def __str__(self):
        return f"{self.name}"
    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')
        ]

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


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
    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "task_manager_task"
        ordering = ["-created_at"]
        verbose_name = "Task"
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_task_title')
        ]


class SubTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtask')
    status = models.CharField(choices=Task.STATUS_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title}"
    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ["-created_at"]
        verbose_name = "SubTask"
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_subtask_title')
        ]

