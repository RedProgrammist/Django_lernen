from django.contrib import admin
from . import models
from .models import SubTask

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ('title', 'description', 'status', 'deadline')
    show_change_link = True


class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'deadline')
    ordering = ('-deadline', 'title',)
    fields = ('title', 'description', 'categories', 'status', 'deadline')
    list_per_page = 5
    inlines = [SubTaskInline]
    def short_title(self, obj):
        if len(obj.title) >= 10:
            return f"'{obj.title[:10]}...'"
        return obj.title
    short_title.short_description = 'Title'

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'deadline')
    ordering = ('-deadline', 'title',)
    fields = ('title', 'description', 'task', 'status', 'deadline')
    list_per_page = 5
    def update_allDone(self, request, queryset):
        queryset.update(status="done")
    update_allDone.short_description = "отметить как выполненные"
    actions = [update_allDone]

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