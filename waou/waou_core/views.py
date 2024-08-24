from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
)
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.utils import timezone
from .models import UserProfile 
from project_management.models import Project, Task
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm

# Check if the user is an admin
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

class HomeView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'waou_core/about.html'

class SignUpView(CreateView):
    model = UserProfile
    form_class = CustomUserCreationForm
    template_name = 'waou_core/signup.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'waou_core/login.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'waou_core/password_reset.html'
    success_url = reverse_lazy("password_reset_done")

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'waou_core/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'waou_core/passsword_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'waou_core/password_reset_complete.html'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'waou_core/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'waou_core/password_change_done.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'waou_core/profile.html'

class EditProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'waou_core/edit_profile.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return self.render_to_response({'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomUserChangeForm(instance=self.request.user)
        return context

class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'waou_core/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = UserProfile.objects.count()
        context['total_roles'] = Group.objects.count()
        context['recent_activities'] = UserProfile.objects.order_by('-last_login')[:5]
        
        users = UserProfile.objects.all()
        user_data = []
        for user in users:
            total_tasks = user.tasks.count()
            completed_tasks = user.tasks.filter(status='done').count()
            in_progress_tasks = user.tasks.filter(status='in_progress').count()
            overdue_tasks = user.tasks.filter(due_date__lt=timezone.now(), status__in=['todo', 'in_progress']).count()
            user_data.append({
                'user': user,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'in_progress_tasks': in_progress_tasks,
                'overdue_tasks': overdue_tasks,
            })
        context['user_data'] = user_data
        context['roles'] = Group.objects.all()
        return context

class UserPerformanceView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = UserProfile
    template_name = 'waou_core/user_performance.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = UserProfile.objects.all()
        user_data = []
        for user in users:
            total_tasks = user.tasks.count()  # Assuming a relationship with Task model
            completed_tasks = user.tasks.filter(status='done').count()
            in_progress_tasks = user.tasks.filter(status='in_progress').count()
            overdue_tasks = user.tasks.filter(due_date__lt=timezone.now(), status__in=['todo', 'in_progress']).count()
            user_data.append({
                'user': user,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'in_progress_tasks': in_progress_tasks,
                'overdue_tasks': overdue_tasks,
            })
        context['user_data'] = user_data
        return context

class CreateRoleView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Group
    fields = ['name']
    template_name = 'waou_core/create_role.html'
    success_url = reverse_lazy('admin_dashboard')

class DeleteRoleView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        role_id = kwargs.get('role_id')
        role = get_object_or_404(Group, id=role_id)
        role.delete()
        return redirect('admin_dashboard')

class EditUserRoleView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'waou_core/edit_user_role.html'

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(UserProfile, id=user_id)
        role_name = request.POST.get('role')

        # Validate role
        try:
            group = Group.objects.get(name=role_name)
        except Group.DoesNotExist:
            return self.render_to_response({'message': 'Invalid role.', 'user': user, 'roles': Group.objects.all()})

        # Prevent non-admins from assigning the 'admin' role
        if request.user.role != 'admin' and role_name == 'admin':
            return self.render_to_response({'message': 'Unauthorized action.', 'user': user, 'roles': Group.objects.all()})

        # Update user's roles
        user.groups.clear()
        user.groups.add(group)
        user.role = role_name
        user.save()

        return redirect('admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(UserProfile, id=user_id)
        roles = Group.objects.all()
        context['user'] = user
        context['roles'] = roles
        return context

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project_management/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Project.objects.all()  # Admins can see all projects
        return Project.objects.filter(tasks__assigned_to=user).distinct()

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'project_management/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all()  # Admins can see all tasks
        return Task.objects.filter(assigned_to=user)

def edit_user_role(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        role_name = request.POST.get('role')
        try:
            group = Group.objects.get(name=role_name)
        except Group.DoesNotExist:
            # Handle error
            return render(request, 'waou_core/error_page.html', {'message': 'The specified role does not exist.'})

        user.groups.clear()
        user.groups.add(group)
        user.role = role_name
        user.save()
        return redirect('admin_dashboard')

    roles = Group.objects.all()
    return render(request, 'waou_core/edit_user_role.html', {'user': user, 'roles': roles})

def delete_role(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    role.delete()
    return redirect('admin_dashboard')