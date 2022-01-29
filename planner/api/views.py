from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from planner.models import Task
from .serializers import TaskSerializer


class TaskListApiView(ListAPIView):

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
