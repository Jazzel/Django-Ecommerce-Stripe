from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    DetailView, CreateView, TemplateView, ListView, View)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView
from .forms import UserForm, UserDetailsForm, ProfileForm
from django.urls import reverse_lazy, reverse
from .models import UserProfile, UserLog
from django.contrib.auth.decorators import login_required


# Create your views here.
User = get_user_model()


class MyProfileView(DetailView):
    template_name = "accounts/my-profile.html"
    queryset = User.objects.all().prefetch_related('posts')

    def get_object(self):
        return get_object_or_404(User, username__iexact=self.kwargs.get('username'))

    def get_context_data(self, *args, **kwargs):
        context = super(MyProfileView, self).get_context_data(*args, **kwargs)
        following = UserProfile.objects.is_following(
            self.request.user, self.get_object())
        context['following'] = following
        context['head'] = 'Profile'
        return context

    # def test_func(self):
    #     return self.request.user.is_superuser


class UserRegisterView(FormView):
    form_class = UserForm
    template_name = 'accounts/registration.html'
    success_url = '/accounts/login'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return super(UserRegisterView, self).form_valid(form)


@login_required
def UserDetailsEditView(request):
    user = get_object_or_404(UserProfile, user=request.user)
    profile_form = ProfileForm(request.POST or None, instance=user)
    user_form = UserDetailsForm(request.POST or None, instance=request.user)

    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            image = request.FILES.get('image')
            bio = request.POST.get('bio')
            social = request.POST.get('social')
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.bio = bio
            user_profile.social = social
            user_profile.image = image
            user_profile.save()
            return HttpResponseRedirect(reverse('account:profile'))

    return render(request, 'dashboard/user.html', {
        'head': 'User Profile',
        'contact_form': user_form,
        'profile_form': profile_form,
    })


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user.html'

    def get_queryset(self):
        queryset = User.objects.get(username=self.request.user.username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['head'] = 'User Profile'
        return context


class UserLogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserLog

    def get_context_data(self, **kwargs):
        context = super(UserLogListView, self).get_context_data(**kwargs)
        context['head'] = 'User Activity'
        context['sub_head'] = 'List'
        return context

    def test_func(self):
        return self.request.user.is_superuser


class UserLogDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserLog

    def get_context_data(self, **kwargs):
        context = super(UserLogDetailView, self).get_context_data(**kwargs)
        context['head'] = 'User Activity'
        context['sub_head'] = 'Details'
        return context

    def test_func(self):
        return self.request.user.is_superuser


class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = "accounts/users.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['head'] = 'Users'
        context['sub_head'] = 'List'
        return context

    def test_func(self):
        return self.request.user.is_superuser


class UserDetailView(UserPassesTestMixin, DetailView):
    model = User
    template_name = "accounts/user_details.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['head'] = 'Users'
        context['sub_head'] = 'Details'
        return context

    def test_func(self):
        return self.request.user.is_superuser
