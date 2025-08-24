from calendar import weekday
from datetime import timezone
from django.db.models import Count
from django.db.models.functions import Extract, ExtractWeekDay
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from myapp import serializers
from myapp.models import Task, SubTask, Category
from myapp.serializers import TaskCreateSerializer, TaskDetailSerializer, SubTaskCreateSerializer, \
    CategoryCreateSerializer
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# Create your views here.

def hello_world(request):
    return HttpResponse("<h1>Hello, world!!!</h1>")

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






class TaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        deadline = self.request.query_params.get('deadline')

        if deadline:
            queryset = queryset.filter(title__icontains=deadline)

        if status:
            queryset = queryset.filter(status=status)
        queryset.order_by('created_at')
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskDetailSerializer
class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('pk')
        return Task.objects.filter(id=task_id)
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskDetailSerializer

class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        deadline = self.request.query_params.get('deadline')

        if deadline:
            queryset = queryset.filter(title__icontains=deadline)

        if status:
            queryset = queryset.filter(status=status)
        queryset.order_by('created_at')
        return queryset
class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('pk')
        return SubTask.objects.filter(id=task_id)



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    def get_queryset(self):
        return Category.objects.filter(is_deleted=False)
    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk):
        category = self.get_object()
        count = category.task.count()
        return Response({'category': category.name, 'task_count': count})

class JWTView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "Hello, ", "user": request.user.username})

