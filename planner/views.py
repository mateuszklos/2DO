import datetime

import xlwt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .forms import CreateUserForm, TaskForm
from .models import Task
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages, auth


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        messages.success(request, 'wiadomosc1')
        return render(request, 'index.html')


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        messages.success(request, 'logged in successfully')
        return redirect('archive')
    else:
        return redirect('index')


class DashboardView(ListView):
    model = Task
    template_name = 'dashboard.html'
    paginate_by = 8

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).filter(is_completed=False).order_by('-created_at')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)


class ArchiveView(ListView):
    model = Task
    template_name = 'archive.html'
    paginate_by = 8

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).filter(is_completed=True).order_by('-completed_at')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArchiveView, self).dispatch(*args, **kwargs)


class SearchResultsView(ListView):
    model = Task
    template_name = 'search_results.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')

        object_list = Task.objects.filter(
            Q(title__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:

        form = CreateUserForm(request.POST)
        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'your account has been created! now you can sign in')
                return redirect('index')

        context = {'form': form}

        return render(request, 'register.html', context)


@login_required
def addtask(request):
    form = TaskForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = User.objects.get(id=request.user.id)
        form.save()

        messages.success(request, 'New task created successfully!')
        return redirect('dashboard')

    return render(request, 'addtask.html', {'form': form})


@login_required
def edittask(request, id):
    task = get_object_or_404(Task, pk=id)

    if task.is_completed:
        messages.success(request, 'You can\'t edit already completed task')
        return redirect('dashboard')
    else:

        form = TaskForm(request.POST or None, request.FILES or None, instance=task)

        if task.user != request.user:
            messages.success(request, 'You can\'t edit someone\'s task')
            return redirect('dashboard')

        if form.is_valid():
            messages.success(request, 'Task edited successfully!')
            form.save()
            return redirect('dashboard')

    return render(request, 'edit.html', {'form': form, 'task': task})


@login_required
def deletetask(request, id):
    task = get_object_or_404(Task, pk=id)

    if task.user != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('dashboard')

    return render(request, 'delete_confirm.html', {'task': task})


@login_required
def completetask(request, id):
    task = get_object_or_404(Task, pk=id)

    if task.user != request.user:
        return redirect('dashboard')

    form = TaskForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.is_completed = True
        task.completed_at = datetime.datetime.now()
        task.save()
        messages.success(request, 'completed!')

        return redirect('dashboard')

    return render(request, 'complete_confirm.html', {'task': task})


@login_required
def statistics(request):
    user = request.user
    tasks_count = Task.objects.all().filter(user=user).count()
    all_tasks = Task.objects.all().filter(user=user)
    completed = Task.objects.all().filter(user=user).filter(is_completed=True).count()
    comp = Task.objects.all().filter(user=user).filter(is_completed=True)[:10]
    uncompleted = Task.objects.all().filter(user=user).filter(is_completed=False).count()
    uncomp = Task.objects.all().filter(user=user).filter(is_completed=False)[:10]
    task_sum = completed + uncompleted

    if task_sum == 0:
        percentage = 0
    else:
        percentage = round(((completed / task_sum) * 100), 1)

    return render(request, 'statistics.html',
                  {"all_tasks": all_tasks, "completed": completed, "uncompleted": uncompleted, "task_sum": task_sum,
                   "percentage": percentage, "tasks_count": tasks_count, "comp": comp, "uncomp": uncomp})


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tasks_' + str(request.user) + '_' + str(
        datetime.datetime.now().strftime("%m/%d/%Y")) + '.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Tasks.xls')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['title', 'created at', 'completed', 'completed at']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Task.objects.all().filter(user=request.user).values_list('title', 'created_at', 'is_completed',
                                                                    'completed_at')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# error handlers

def handler403(request):
    return render(request, 'errors/403.html', status=403)


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)

# TODO: komunikat zle login/haslo przy logowaniu
# TODO: favicon
# TODO: poprawic kod i deploy!!!!!!!
