from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,PasswordChangeView, PasswordChangeDoneView
from .models import UserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'waou_core/about.html')

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
    success_url =  reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'waou_core/password_reset_complete.html'
    
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'waou_core/password_change_form.html'
    success_url = reverse_lazy('password_change_done')
    
class CustomePasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'waou_core/password_change_done.html'
       
@login_required
def profile_view(request):
    return render(request, 'waou_core/profile.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after successful edit
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'waou_core/edit_profile.html', {'form': form})

