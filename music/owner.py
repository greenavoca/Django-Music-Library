from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from core.models import Profile

class OwnerListView(LoginRequiredMixin, ListView):
    """Sub-class."""
    login_url = 'signin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_object = User.objects.get(username=self.request.user.username)
        profile_object = Profile.objects.get(user=user_object)
        context["profile_object"] = profile_object
        return context

class OwnerCreateView(LoginRequiredMixin, CreateView):
    login_url = 'signin'
    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_object = User.objects.get(username=self.request.user.username)
        profile_object = Profile.objects.get(user=user_object)
        context["profile_object"] = profile_object
        return context

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'signin'
    def get_queryset(self):
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_object = User.objects.get(username=self.request.user.username)
        profile_object = Profile.objects.get(user=user_object)
        context["profile_object"] = profile_object
        return context

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'signin'
    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_object = User.objects.get(username=self.request.user.username)
        profile_object = Profile.objects.get(user=user_object)
        context["profile_object"] = profile_object
        return context