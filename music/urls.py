from django.urls import path
from . import views

app_name = 'music'
urlpatterns = [
    path('', views.MusicListView.as_view(), name='all'),
    path('track/create', views.MusicCreateView.as_view(), name='music_create'),
    path('track/<int:pk>/update', views.MusicUpdateView.as_view(), name='music_update'),
    path('track/<int:pk>/delete', views.MusicDeleteView.as_view(), name='music_delete'),
]