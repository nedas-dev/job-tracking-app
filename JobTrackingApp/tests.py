from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from . import views
from .models import ScheduleEvent, Client
import datetime

# Testing index view (events view)
class EventsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.userInstance = User.objects.create_user(username='testUser', password='password123')

        cls.clientInstance = Client.objects.create(user=cls.userInstance, name='Michael Rodrigo', address='whatever 123')

        cls.eventInstance = ScheduleEvent.objects.create(date=datetime.date.today(), duration='', client=cls.clientInstance, description='apples are apples')
    
    def setUp(self):
        ''' Both login ways are valid! 
        self.client.login(username='testUser', password='password123')
        '''

        self.client.post(reverse('login'), {'username':'testUser', 'password': 'password123'})

    def test_home_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(url, '/')
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

    def test_edit_event_view_status_code(self):
        url = reverse('editEvent',kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(url, '/events/1/edit')
        self.assertEquals(response.status_code, 200)

    def test_edit_event_template_names(self):
        url = reverse('editEvent', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.templates[0].name, 'JobTrackingApp/eventEditView.html')
    
    def test_edit_event_func_name(self):
        url = reverse('editEvent', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.resolver_match.func, views.editEvent)
        self.assertEquals(response.resolver_match.view_name, 'editEvent')
    
    def test_edit_event_POST_redirect(self):
        url = reverse('editEvent', kwargs={'pk': 1})
        response = self.client.post(url, {
            'date': "12/24/2018", 
            'duration': '1hr', 
            'work_order': '-',
            'client': '1',
            'description': 'nedys'}, follow=True)
            
        redirect_url, status_code = response.redirect_chain[0]
        self.assertEquals(redirect_url, reverse('index'))
        self.assertEquals(status_code, 302)
