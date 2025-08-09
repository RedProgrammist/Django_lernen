from datetime import timezone
from django.db.models import Count
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView

from myapp import serializers
from myapp.models import Task
from myapp.serializers import TaskCreateSerializer, TaskDetailSerializer


# Create your views here.

def hello_world(request):
    return HttpResponse("<h1>Hello, world!</h1>")

@api_view(['POST'])
def task_create(request):
    serializer = serializers.TaskModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def tasks_list(request):
    tasks = Task.objects.all()
    serializer = serializers.TaskDetailSerializer(tasks, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def tasks_byid(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({'error': 'Es gibt keine Aufgabe'},status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.TaskDetailSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def tasks_stat(request):
    task_cnt = Task.objects.aggregate(task_count=Count('id'))
    task_cnt_stat = Task.objects.values('status').annotate(task_count=Count('id'))
    task_prosr = Task.objects.filter(deadline__gt=timezone.now())
    task_prosr_serialized = serializers.TaskModelSerializer(task_prosr, many=True).data
    return Response({'total_tasks': task_cnt,'by_status': task_cnt_stat,'prosr_tasks': task_prosr_serialized})


# Создайте классы представлений для создания и получения списка подзадач (SubTaskListCreateView).
#
# Создайте классы представлений для получения, обновления и удаления подзадач (SubTaskDetailUpdateDeleteView).




class TaskListCreateView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailUpdateDeleteView(APIView):
    def get(self, request, id):
     try:
        task = Task.objects.get(id=id)
     except Task.DoesNotExist:
        return Response({'error': 'Es gibt keine Aufgabe'}, status=status.HTTP_404_NOT_FOUND)
     serializer = TaskDetailSerializer(task)
     return Response(serializer.data)

    def put(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response({'error': 'Es gibt keine Aufgabe'},status=status.HTTP_404_NOT_FOUND)
        serializer = TaskCreateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except:
            return Response({'error': 'Es gibt keine Aufgabe'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
