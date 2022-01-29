from rest_framework import serializers
from planner.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['user', 'title', 'created_at', 'is_completed', 'completed_at']