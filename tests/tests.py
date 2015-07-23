import json

from django.test import TestCase
from django.core.urlresolvers import reverse


class LazyTagsViewTests(TestCase):

    def test_tag_with_no_args_or_kwargs(self):
        url = reverse('lazy_tag')

        response = self.client.get(url, {'tag': 'test_tags.test'})

        self.assertEqual(response.content, 'hello world')

    def test_tag_with_just_args(self):
        url = reverse('lazy_tag')
        data = {
            'tag': 'test_tags.test_with_args',
            'args': json.dumps(['hello']),
        }

        response = self.client.get(url, data)

        expected_html = '<p>hello</p>'
        self.assertHTMLEqual(response.content, expected_html)

    def test_tag_with_args_and_kwargs(self):
        url = reverse('lazy_tag')
        data = {
            'tag': 'test_tags.test_with_args',
            'args': json.dumps(['hello']),
            'kwargs': json.dumps({'kwarg': 'world'}),
        }

        response = self.client.get(url, data)

        expected_html = '<p>hello</p><p>world</p>'
        self.assertHTMLEqual(response.content, expected_html)

    def test_inclusion_tag(self):
        url = reverse('lazy_tag')

        response = self.client.get(url, {'tag': 'test_tags.inclusion'})

        expected_html = '<p>hello world</p>'
        self.assertHTMLEqual(response.content, expected_html)
