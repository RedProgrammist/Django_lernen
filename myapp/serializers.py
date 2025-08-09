from datetime import timezone

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
        fields = '__all__'

    def create(self, validated_data):
        if Category.object.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует.'})
        return Category.object.create(**validated_data)

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
    def validate_deadline(value):
        if value < timezone.now():
            raise serializers.ValidationError("Es ist yu fruh")
    deadline = serializers.DateTimeField(validators=[validate_deadline])
    class Meta:
        model = Task
        fields = '__all__'


