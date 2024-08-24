from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, Task
from .forms import ProjectForm, TaskForm


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        user = self.request.user
        return user.role in self.allowed_roles or user.role == 'admin'  # Allow admins full access


# Project Views
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project_management/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Project.objects.all()  # Admins can see all projects
        # Get the set of projects where the user is assigned tasks
        return Project.objects.filter(tasks__assigned_to=user).distinct()
    


class ProjectCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_management/project_form.html'
    success_url = reverse_lazy('project_list')
    allowed_roles = ['admin']


class ProjectDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Project
    template_name = 'project_management/project_detail.html'
    allowed_roles = ['admin']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Project.objects.all()  # Admins can see all projects
        return Project.objects.filter(team=user).distinct()


class ProjectUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_management/project_form.html'
    success_url = reverse_lazy('project_list')
    allowed_roles = ['admin']


class ProjectDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_management/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')
    allowed_roles = ['admin']


# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'project_management/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all()  # Admins can see all tasks
        return Task.objects.filter(assigned_to=user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'project_management/task_detail.html'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all()  # Admins can see all tasks
        return Task.objects.filter(assigned_to=user)


class TaskCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'project_management/task_form.html'
    success_url = reverse_lazy('task_list')
    allowed_roles = ['admin']


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'project_management/task_form.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        user = self.request.user
        task = self.get_object()
        return user.role == 'admin' or task.assigned_to == user


class TaskDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Task
    template_name = 'project_management/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    allowed_roles = ['admin']


# Custom 403 handler
def permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)
