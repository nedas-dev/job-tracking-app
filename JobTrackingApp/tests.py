from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from . import views

# Create your tests here.
class IndexTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='nedukas1998', password='nedukas111')
    
    def setUp(self):
        ''' Both login ways are valid! 
        self.client.login(username='nedukas1998', password='nedukas111')
        '''

        self.client.post(reverse('login'), {'username':'nedukas1998', 'password': 'nedukas111'})

    def test_home_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_home_view_template_names(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.templates[0].name, 'JobTrackingApp/index.html')
        self.assertEquals(response.templates[1].name, 'JobTrackingApp/base.html')
    
    def test_home_view_func_name(self):
        url = reverse('index')
        response = self.client.get(url)
        # response.resolver_match is equal to resolve(url)
        self.assertEquals(response.resolver_match.func, views.index)
        self.assertEquals(response.resolver_match.view_name, 'index')