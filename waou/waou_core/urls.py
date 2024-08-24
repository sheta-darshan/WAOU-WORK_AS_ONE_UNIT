from django.urls import path
from .views import (
    HomeView, AboutView, SignUpView, CustomLoginView, CustomPasswordResetView,
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
    CustomPasswordChangeView, CustomPasswordChangeDoneView, ProfileView, EditProfileView,
    AdminDashboardView, UserPerformanceView, CreateRoleView, DeleteRoleView, EditUserRoleView,
    ProjectListView, TaskListView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('user-performance/', UserPerformanceView.as_view(), name='user_performance'),
    path('create-role/', CreateRoleView.as_view(), name='create_role'),
    path('delete-role/<int:role_id>/', DeleteRoleView.as_view(), name='delete_role'),
    path('edit-user-role/<int:user_id>/', EditUserRoleView.as_view(), name='edit_user_role'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
]