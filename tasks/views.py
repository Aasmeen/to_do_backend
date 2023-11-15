from django.db.models import Count, Case, When, IntegerField
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from tasks.serializers import TaskSerializer
from tasks.models import Tasks

class BaseAPIView(APIView):
    """
    Base API to get basic user details
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Method to get basic user related details
        returns {
            'first_name': <user_first_name>,
            'last_name': <user_'last_name'>,
            'incomplete_task': <number_of_incompleted_task>,
            'important_task': <number_of_important_task>
        }
        """
        user = request.user
        task_counts = Tasks.objects.filter(user_id=user.id).aggregate(
            incompleted_tasks=Count(
                Case(When(is_completed=False, then=1), output_field=IntegerField())
            ),
            important_task=Count(
                Case(When(is_important=True, then=1), output_field=IntegerField())
            )
        )
        return Response({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'incomplete_task': task_counts.get('incompleted_tasks', 0),
            'important_task': task_counts.get('important_task', 0),
        })


class TaskAPIView(ModelViewSet):
    """
    API view to handle task related requests
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        method to return Task queryset
        """
        return Tasks.objects.filter(user_id=self.request.user.id).order_by('schedule')

    def filter_queryset(self, queryset):
        """
        method to filter queryset
        """
        search_title = self.request.query_params.get('search')
        if search_title:
            queryset = queryset.filter(title__icontains=search_title)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        method to create task
        """
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        method to get list of user related task
        """
        queryset = self.filter_queryset(self.get_queryset())
        incomplete_task_queryset = queryset.filter(is_completed=False)
        incomplete_task = self.get_serializer(incomplete_task_queryset, many=True)
        complete_task_queryset = queryset.filter(is_completed=True)
        complete_task = self.get_serializer(complete_task_queryset, many=True)
        return Response({
            'incomplete_task': incomplete_task.data,
            'complete_task': complete_task.data
        })

