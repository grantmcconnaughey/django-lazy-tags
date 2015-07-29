import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse

from lazy_tags.templatetags import lazy_tags
from lazy_tags.utils import get_tag_html


class LazyTagsViewTests(TestCase):

    def test_tag_with_no_args_or_kwargs(self):
        url = reverse('lazy_tag')

        response = self.client.get(url, {'tag': 'test_tags.test'})

        self.assertEqual(response.content.decode(), '<p>hello world</p>')

    def test_tag_with_just_args(self):
        url = reverse('lazy_tag')
        data = {
            'tag': 'test_tags.test_with_args',
            'args': json.dumps(['hello']),
        }

        response = self.client.get(url, data)

        self.assertHTMLEqual(response.content.decode(), '<p>hello</p>')

    def test_tag_with_args_and_kwargs(self):
        url = reverse('lazy_tag')
        data = {
            'tag': 'test_tags.test_with_args',
            'args': json.dumps(['hello']),
            'kwargs': json.dumps({'kwarg': 'world'}),
        }

        response = self.client.get(url, data)

        self.assertHTMLEqual(response.content.decode(), '<p>hello world</p>')

    def test_inclusion_tag(self):
        url = reverse('lazy_tag')

        response = self.client.get(url, {'tag': 'test_tags.inclusion'})

        self.assertHTMLEqual(response.content.decode(), '<p>hello world</p>')

    @override_settings(LAZY_TAGS_FORCE_LOGIN=True)
    def test_force_login_not_logged_in(self):
        url = reverse('lazy_tag')

        response = self.client.get(url, {'tag': 'test_tags.test'})

        self.assertEqual(response.status_code, 403)

    @override_settings(LAZY_TAGS_FORCE_LOGIN=True)
    def test_force_login_logged_in(self):
        user = User.objects.create_user('test',
                                        'test@gmail.com',
                                        'password')
        self.client.login(username=user.username, password='password')
        url = reverse('lazy_tag')

        response = self.client.get(url, {'tag': 'test_tags.test'})

        self.assertEqual(response.status_code, 200)
        self.client.logout()


class LazyTagsTests(TestCase):

    def setUp(self):
        self.context = {
            'lazy_tag_data': {
                'tag': 'test_tags.tag',
                'args': json.dumps([]),
                'kwargs': json.dumps({}),
            },
        }

    def test_default_error_message(self):
        html = lazy_tags.lazy_tags_js(self.context)

        self.assertIn('An error occurred.', html)

    @override_settings(LAZY_TAGS_ERROR_MESSAGE='<p>Custom error message!</p>')
    def test_custom_error_message(self):
        html = lazy_tags.lazy_tags_js(self.context)

        self.assertIn('<p>Custom error message!</p>', html)


class LazyTagsUtilsTests(TestCase):

    def test_get_tag_html_kwargs_works_with_strings(self):
        html = get_tag_html('lib.tag_name', args=None,
                            kwargs='{"test": "hello", "test2": "world"}')

        self.assertEqual(html, "{% load lib %}{% tag_name test='hello' test2='world' %}")

    def test_get_tag_html_kwargs_works_with_ints(self):
        html = get_tag_html('lib.tag_name', args=None, kwargs='{"test": 123}')

        self.assertEqual(html, "{% load lib %}{% tag_name test=123 %}")

    def test_get_tag_html_kwargs_works_with_floats(self):
        html = get_tag_html('lib.tag_name', args=None, kwargs='{"test": 1.23}')

        self.assertEqual(html, "{% load lib %}{% tag_name test=1.23 %}")

    def test_get_tag_html_args_works_with_strings(self):
        html = get_tag_html('lib.tag_name', args='["hello", "world"]')

        self.assertEqual(html, "{% load lib %}{% tag_name 'hello' 'world' %}")

    def test_get_tag_html_args_works_with_ints(self):
        html = get_tag_html('lib.tag_name', args='[123, 456]')

        self.assertEqual(html, "{% load lib %}{% tag_name 123 456 %}")

    def test_get_tag_html_args_works_with_ints(self):
        html = get_tag_html('lib.tag_name', args='[1.23, 4.56]')

        self.assertEqual(html, "{% load lib %}{% tag_name 1.23 4.56 %}")
