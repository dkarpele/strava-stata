from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView


class ProfileUser(ListView):
    model = get_user_model()
    template_name = 'users/profile.html'
    extra_context = {
        'title': "User profile",
        #'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('stata:home')