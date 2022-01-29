from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

import planner
from .views import DashboardView, register, addtask, SearchResultsView, deletetask, edittask, completetask,\
    ArchiveView, statistics, export_excel
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('', LoginView.as_view(template_name='index.html', redirect_authenticated_user=True), name='index'),
    path('login/', LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name="register"),
    path('statistics/', statistics, name="statistics"),
    path('export/', export_excel, name="export"),
    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),
    path('archive/', login_required(ArchiveView.as_view()), name='archive'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('add/', addtask, name='addtask'),
    path('delete/<int:id>', deletetask, name='deletetask'),
    path('edit/<int:id>', edittask, name='edittask'),
    path('complete/<int:id>', completetask, name='completetask'),
    path('api/', include('planner.api.urls')),

]


handler404 = planner.views.handler404
handler500 = planner.views.handler500

