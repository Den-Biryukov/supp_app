from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from support.models import Ticket, Support, Comment
from rest_framework import status
import json


class TicketAPITestCase(APITestCase):

    def setUp(self):

        self.admin = User.objects.create(email='admin@mail.ru', username='admin',
                                         password='test_password123', is_staff=True)

        self.user = User.objects.create(email='test@mail.ru', username='test_user',
                                        password='test_password123')

        self.user_support = User.objects.create(email='test_support@mail.ru', username='test_user_support',
                                                password='test_password123')

        self.support = Support.objects.create(user=self.user_support, is_support=True)

        self.ticket = Ticket.objects.create(ticket_name='test ticket', user=self.user,
                                            description='some problem')

    def test_check_users_ticket(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(self.user_support.supports.is_support, True)

    def test_get_not_authenticated(self):
        url = 'http://127.0.0.1:8000/api/v1/ticket/'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get(self):
        url = 'http://127.0.0.1:8000/api/v1/ticket/'
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_not_authenticated(self):
        self.assertEqual(Ticket.objects.count(), 1)
        url = 'http://127.0.0.1:8000/api/v1/ticket/'
        data = {
            'ticket_name': 'another one problem',
            'description': 'something is not working'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_create_ticket(self):
        self.assertEqual(Ticket.objects.count(), 1)
        url = 'http://127.0.0.1:8000/api/v1/ticket/'
        data = {
            'ticket_name': 'another one problem',
            'description': 'something is not working'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertEqual(self.user, Ticket.objects.last().user)

    def test_change_status_support(self):
        self.assertEqual(Ticket.objects.get(id=1).status, 0)
        url = 'http://127.0.0.1:8000/api/v1/ticket_support/1/'
        data = {
            'status': 2
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_support)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.ticket.refresh_from_db()
        self.assertEqual(Ticket.objects.get(id=1).status, 2)

    def test_change_status_admin(self):
        self.assertEqual(Ticket.objects.get(id=1).status, 0)
        url = 'http://127.0.0.1:8000/api/v1/ticket_support/1/'
        data = {
            'status': 2
        }
        json_data = json.dumps(data)
        self.client.force_login(self.admin)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.ticket.refresh_from_db()
        self.assertEqual(Ticket.objects.get(id=1).status, 2)

    def test_change_status_user(self):
        self.assertEqual(Ticket.objects.get(id=1).status, 0)
        url = 'http://127.0.0.1:8000/api/v1/ticket_support/1/'
        data = {
            'status': 1
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Ticket.objects.get(id=1).status, 0)

    def test_create_comment(self):
        self.assertEqual(Comment.objects.all().count(), 0)
        url = 'http://127.0.0.1:8000/api/v1/comment/'
        data = {
            'content': 'some content',
            'ticket': 1,
            'parent': None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(self.user, Comment.objects.first().user)
