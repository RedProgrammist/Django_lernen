import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # путь к settings.py
django.setup()

from django.db.models import Q
from myapp.models import *
from django.utils import timezone
from datetime import timedelta

cat = Category.objects.create(name = 'h10')

t1 = Task.objects.create(
    title = "Prepare presentation",
    description = "Prepare materials and slides for the presentation",
    status = "New",
    deadline = timezone.now() + timedelta(days=3))
t1.categories.set([cat])

st1 = SubTask.objects.create(
    title = "Gather information",
    description = "Find necessary information for the presentation",
    task = t1,
    status = "New",
    deadline = timezone.now() + timedelta(days=2))


st2 = SubTask.objects.create(
    title = "Create slides",
    description = "Create presentation slides",
    task = t1,
    status = "New",
    deadline = timezone.now() + timedelta(days=1))


new_task = Task.objects.filter(status__iexact = "New")

for task in new_task:
    print(task)

prosr_subtask = SubTask.objects.filter(Q(status__iexact = "Done") & Q(deadline__lt=timezone.now()))

for subtask in prosr_subtask:
    print(subtask)


t1.status = "In progress"
st1.deadline = st1.deadline - timedelta(days=2)
st2.description = "Create and format presentation slides"

t1.delete()