import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse

from lazy_tags.templatetags import lazy_tags
from lazy_tags.utils import get_tag_html, set_lazy_tag_data


class LazyTagsViewTests(TestCase):

    def test_tag_with_no_args_or_kwargs(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'test_tags.test')
        url = reverse('lazy_tag', args=[tag_id])

        response = self.client.get(url)

        self.assertEqual(response.content.decode(), '<p>hello world</p>')

    def test_tag_with_just_args(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'test_tags.test_with_args', ['hello'])
        url = reverse('lazy_tag', args=[tag_id])

        response = self.client.get(url)

        self.assertHTMLEqual(response.content.decode(), '<p>hello</p>')

    def test_tag_with_args_and_kwargs(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'test_tags.test_with_args',
                            ['hello'], {'kwarg': 'world'})
        url = reverse('lazy_tag', args=[tag_id])

        response = self.client.get(url)

        self.assertHTMLEqual(response.content.decode(), '<p>hello world</p>')

    def test_inclusion_tag(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'test_tags.inclusion')
        url = reverse('lazy_tag', args=[tag_id])

        response = self.client.get(url)

        self.assertHTMLEqual(response.content.decode(), '<p>hello world</p>')

    # def test_tag_with_django_orm(self):
    #     user = User.objects.create_user('test',
    #                                     'test@gmail.com',
    #                                     'password')
    #     tag_id = str(uuid.uuid4())
    #     set_lazy_tag_data(tag_id, 'test_tags.test_orm', [user])
    #     url = reverse('lazy_tag', args=[tag_id])

    #     response = self.client.get(url)

    #     self.assertHTMLEqual(response.content.decode(), '<p>test | test@gmail.com</p>')


class LazyTagsTests(TestCase):

    def test_default_error_message(self):
        html = lazy_tags.lazy_tags_js()

        self.assertIn('An error occurred.', html)

    @override_settings(LAZY_TAGS_ERROR_MESSAGE='<p>Custom error message!</p>')
    def test_custom_error_message(self):
        html = lazy_tags.lazy_tags_js()

        self.assertIn('<p>Custom error message!</p>', html)


class LazyTagsUtilsTests(TestCase):

    def test_get_tag_html_kwargs_works_with_strings(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'lib.tag_name', None, {'test': 'hello'})

        html = get_tag_html(tag_id)

        self.assertEqual(html, "{% load lib %}{% tag_name test='hello' %}")

    def test_get_tag_html_kwargs_works_with_ints(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'lib.tag_name', None, {'test': 123})

        html = get_tag_html(tag_id)

        self.assertEqual(html, "{% load lib %}{% tag_name test=123 %}")

    def test_get_tag_html_kwargs_works_with_floats(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'lib.tag_name', None, {'test': 1.23})

        html = get_tag_html(tag_id)

        self.assertEqual(html, "{% load lib %}{% tag_name test=1.23 %}")

    def test_get_tag_html_args_works_with_strings(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'lib.tag_name', ['hello', 'world'])

        html = get_tag_html(tag_id)

        self.assertEqual(html, "{% load lib %}{% tag_name 'hello' 'world' %}")

    def test_get_tag_html_args_works_with_ints(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'lib.tag_name', [123, 456])

        html = get_tag_html(tag_id)

        self.assertEqual(html, "{% load lib %}{% tag_name 123 456 %}")

    def test_get_tag_html_args_works_with_ints(self):
        tag_id = str(uuid.uuid4())
        set_lazy_tag_data(tag_id, 'lib.tag_name', [1.23, 4.56])

        html = get_tag_html(tag_id)

        self.assertEqual(html, "{% load lib %}{% tag_name 1.23 4.56 %}")
