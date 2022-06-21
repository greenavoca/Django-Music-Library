from django.shortcuts import render
from .models import Song
from .owner import OwnerDeleteView, OwnerCreateView, OwnerUpdateView, OwnerListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from core.models import Profile


# Create your views here.

class MusicListView(OwnerListView):
    model = Song

    def get(self, request):
        sg = Song.objects.filter(owner=request.user.id).count()
        sa = Song.objects.all()
        user_object = User.objects.get(username=self.request.user.username)
        profile_object = Profile.objects.get(user=user_object)
        ctx = {"song_count": sg, "music_list": sa, "profile_object": profile_object}
        return render(request, 'music/song_list.html', ctx)


class MusicCreateView(OwnerCreateView):
    model = Song
    fields = ['artist', 'title', 'genre']
    success_url = reverse_lazy('music:all')

class MusicUpdateView(OwnerUpdateView):
    model = Song
    fields = ['artist', 'title', 'genre']
    success_url = reverse_lazy('music:all')

class MusicDeleteView(OwnerDeleteView):
    model = Song
    success_url = reverse_lazy('music:all')

