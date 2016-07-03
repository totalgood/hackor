from django.core.urlresolvers import resolve
from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from guess.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_post_request_resolves_to_results(self):
        c = Client()
        response = c.post('/sketch/', {'info': '2'})
        self.assertEqual(response.status_code, 200)
