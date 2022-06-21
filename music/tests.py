from django.test import TestCase, Client, RequestFactory
from core.models import Profile
from django.contrib.auth.models import User
from .models import Song
from django.urls import reverse
from . import views


class TestMusicApp(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_a = User.objects.create_user(username='test_user', email='test@django.com', password='test1234')
        self.user_a.is_staff = True
        self.user_a.is_superuser = True
        self.profile_object = Profile.objects.create(user=self.user_a, id_user=self.user_a.id)
        self.factory = RequestFactory()
        self.song = Song.objects.create(title='test', artist='test', genre='test', owner=self.user_a)

    def test_model_str(self):
        self.assertEqual(str(self.song), 'test - test')

    def test_music_list_view(self):
        self.client.login(username='test_user', password='test1234')
        response = self.client.get(reverse('music:all'))
        self.assertEqual(response.status_code, 200)

    def test_music_list_view_context(self):
        request = self.factory.get(reverse('music:all'))
        request.user = self.user_a
        view = views.MusicListView()
        view.setup(request)
        view.object_list = view.get_queryset()

        context = view.get_context_data()
        self.assertIn('profile_object', context)

    def test_music_create_view_context(self):
        request = self.factory.post(reverse('music:music_create'))
        request.user = self.user_a
        view = views.MusicCreateView()
        view.setup(request)
        view.object_list = view.get_queryset()
        view.object = self.profile_object

        context = view.get_context_data()
        self.assertIn('profile_object', context)

    def test_music_create_view(self):
        self.client.login(username='test_user', password='test1234')
        data = {'artist': 'test',
                'title': 'test',
                'genre': 'test'
        }
        response = self.client.post(reverse('music:music_create'), data)
        self.assertEqual(response.status_code, 302)

    def test_music_update_view_context(self):
        request = self.factory.post(reverse('music:music_update', args=[self.song.id]))
        request.user = self.user_a
        view = views.MusicUpdateView()
        view.setup(request)
        view.object_list = view.get_queryset()
        view.object = self.profile_object

        context = view.get_context_data()
        self.assertIn('profile_object', context)

    def test_music_delete_view_context(self):
        request = self.factory.post(reverse('music:music_delete', args=[self.song.id]))
        request.user = self.user_a
        view = views.MusicDeleteView()
        view.setup(request)
        view.object_list = view.get_queryset()
        view.object = self.profile_object

        context = view.get_context_data()
        self.assertIn('profile_object', context)
