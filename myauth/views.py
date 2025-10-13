from django.contrib.auth.views import LogoutView
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileForm
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class CustomLogoutView(LogoutView):
    next_page = '/auth/login/'

class SetCookieView(View):
    def get(self, request):
        response = HttpResponse("Cookie установлено")
        response.set_cookie('my_cookie', 'example_value', max_age=3600)
        return response

class GetCookieView(View):
    def get(self, request):
        value = request.COOKIES.get('my_cookie', 'Значение отсутствует')
        return HttpResponse(f'Значение cookie: {value}')

class SetSessionView(View):
    def get(self, request):
        request.session['my_session'] = 'session_value'
        return HttpResponse("Сессия установлена")

class GetSessionView(View):
    def get(self, request):
        value = request.session.get('my_session', 'Значение отсутствует')
        return HttpResponse(f'Значение сессии: {value}')

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        return super().form_valid(form)

class AboutMeView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ('avatar',)
    template_name = 'myauth/about_me.html'
    success_url = reverse_lazy('myAuth:about_me')

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'myauth/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('myAuth:user_detail', kwargs={'pk': self.object.user.pk})

    def test_func(self):
        profile = self.get_object()
        user = self.request.user
        return user.is_staff or user == profile.user


class UserListView(ListView):
    model = User
    template_name = 'myauth/user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'myauth/user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object.profile
        user = self.request.user
        context['profile'] = profile
        context['can_edit'] = user.is_staff or user == self.object
        return context