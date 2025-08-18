from django.utils import timezone

from rest_framework import serializers

from myapp.models import *


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = '__all__'

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует.'})
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if Category.objects.filter(name=validated_data['name']).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует.'})
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class TaskDetailSerializer(serializers.ModelSerializer):
    subtask = SubTaskCreateSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'

class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Es ist yu fruh")
        return value

