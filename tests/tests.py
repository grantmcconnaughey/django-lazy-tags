import json

from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse

from lazy_tags.templatetags import lazy_tags


class LazyTagsViewTests(TestCase):

    def test_tag_with_no_args_or_kwargs(self):
        url = reverse('lazy_tag')

        response = self.client.get(url, {'tag': 'test_tags.test'})

        self.assertEqual(str(response.content), '<p>hello world</p>')

    def test_tag_with_just_args(self):
        url = reverse('lazy_tag')
        data = {
            'tag': 'test_tags.test_with_args',
            'args': json.dumps(['hello']),
        }

        response = self.client.get(url, data)

        expected_html = '<p>hello</p>'
        self.assertHTMLEqual(str(response.content), expected_html)

    def test_tag_with_args_and_kwargs(self):
        url = reverse('lazy_tag')
        data = {
            'tag': 'test_tags.test_with_args',
            'args': json.dumps(['hello']),
            'kwargs': json.dumps({'kwarg': 'world'}),
        }

        response = self.client.get(url, data)

        expected_html = '<p>hello world</p>'
        self.assertHTMLEqual(str(response.content), expected_html)

    def test_inclusion_tag(self):
        url = reverse('lazy_tag')

        response = self.client.get(url, {'tag': 'test_tags.inclusion'})

        expected_html = '<p>hello world</p>'
        self.assertHTMLEqual(str(response.content), expected_html)


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
