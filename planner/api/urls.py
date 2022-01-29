from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (
    TaskListApiView,
)

urlpatterns = [
    path('', login_required(TaskListApiView.as_view()), name='task_api')
]