from django.test import TestCase, RequestFactory, Client
from core.models import Profile
from core import views
from django.urls import reverse
from django.core.files.images import ImageFile
from django.contrib.auth.models import User


class TestCoreApp(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_a = User.objects.create_user(username='test_user', email='test@django.com', password='test1234')
        self.user_a.is_staff = True
        self.user_a.is_superuser = True
        self.profile_object = Profile.objects.create(user=self.user_a, id_user=self.user_a.id)
        self.factory = RequestFactory()

    def test_model_str(self):
        self.assertEqual(str(self.profile_object), 'test_user')

    def test_user_exist(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)

    def test_user_password(self):
        self.assertTrue(self.user_a.check_password('test1234'))

    def test_url_home_auth(self):
        request = self.factory.get('/')
        request.user = self.user_a
        response = views.index(request)
        self.assertEqual(response.status_code, 200)

    def test_url_home_not_auth(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.post(reverse('signup'), {
                                               'username': 'test_user1',
                                               'email': 'test1@django.com',
                                               'password': 'test1234',
                                               'password2': 'test1234'
                                               })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('settings'))

    def test_signup_username_taken(self):
        response = self.client.post(reverse('signup'), {
                                               'username': 'test_user',
                                               'email': 'test1@django.com',
                                               'password': 'test1234',
                                               'password2': 'test1234'
                                               })
        self.assertEqual(response.status_code, 302)

    def test_signup_email_taken(self):
        response = self.client.post(reverse('signup'), {
                                               'username': 'test_user1',
                                               'email': 'test@django.com',
                                               'password': 'test1234',
                                               'password2': 'test1234'
                                               })
        self.assertEqual(response.status_code, 302)

    def test_signup_password_not_matching(self):
        response = self.client.post(reverse('signup'), {
                                               'username': 'test_user1',
                                               'email': 'test1@django.com',
                                               'password': 'test1234',
                                               'password2': 'test4321'
                                               })
        self.assertEqual(response.status_code, 302)

    def test_signup_url(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signin(self):
        response = self.client.post(reverse('signin'), {'username': 'test_user', 'password': 'test1234'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_signin_invalid(self):
        response = self.client.post(reverse('signin'), {'username': 'test_user1', 'password': 'test1234'})
        self.assertEqual(response.status_code, 302)

    def test_signin_url(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)

    def test_signin_logged_user(self):
        self.client.login(username='test_user', password='test1234')
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_logout(self):
        self.client.login(username='test_user', password='test1234')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('signin'))

    def test_settings(self):
        self.client.login(username='test_user', password='test1234')
        response = self.client.post(reverse('settings'), {'about': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_settings_upload_img(self):
        self.client.login(username='test_user', password='test1234')
        with open('core/static/test/test.jpeg', 'rb') as image:
            test_file = ImageFile(image)
            response = self.client.post(reverse('settings'), {'image': test_file, 'about': 'test'})
            self.assertEqual(response.status_code, 302)

    def test_profile(self):
        self.client.login(username='test_user', password='test1234')
        response = self.client.get(reverse('profile', args=[self.user_a.username]))
        self.assertEqual(response.status_code, 200)
