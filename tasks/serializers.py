from rest_framework import serializers
from tasks.models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task
    """
    class Meta:
        model = Tasks
        fields = ('id', 'title', 'is_completed', 'is_important', 'user', 'schedule', 'reminder')
        extra_kwargs = {
            'title': {'required': True},
            'user': {'write_only': True},
        }
        read_only = ('id', )
