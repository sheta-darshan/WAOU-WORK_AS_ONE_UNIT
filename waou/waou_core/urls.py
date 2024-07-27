from django.urls import path
from waou_core.views import about, home_view, SignUpView, CustomLoginView, CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, profile_view, edit_profile_view,CustomPasswordChangeView,CustomePasswordChangeDoneView
from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('', views.home, name="home"),
#     path('login/', views.login, name="login"),
#     path('signup/', views.signup, name="signup"),
#     path('about/', views.about, name="about"),
#     path('profile/', views.profile, name="profile"),
# ]

urlpatterns = [
    path('', home_view, name="home"),
    path('about/', about, name="about"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomePasswordChangeDoneView.as_view(), name='password_change_done'),
]