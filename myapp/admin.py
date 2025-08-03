from django.contrib import admin
from . import models

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'deadline')
    ordering = ('-deadline', 'title',)
    fields = ('title', 'description', 'categories', 'status', 'deadline')
    list_per_page = 5

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'deadline')
    ordering = ('-deadline', 'title',)
    fields = ('title', 'description', 'task', 'status', 'deadline')
    list_per_page = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fields = ('name',)
    list_per_page = 5

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.SubTask, SubTaskAdmin)