import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from lazy_tags.templatetags import lazy_tags
from lazy_tags.utils import (
    get_tag_html, set_lazy_tag_data, get_lib_and_tag_name
)

from .templatetags import test_tags


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


class LazyTagsTests(TestCase):

    def test_default_error_message(self):
        html = lazy_tags.lazy_tags_js()

        self.assertIn('An error occurred.', html)

    @override_settings(LAZY_TAGS_ERROR_MESSAGE='<p>Custom error message!</p>')
    def test_custom_error_message(self):
        html = lazy_tags.lazy_tags_js()

        self.assertIn('<p>Custom error message!</p>', html)

    def test_decorated_tag_renders_html(self):
        result = test_tags.test_simple_dec_args(1, kwarg='hello')

        self.assertIn('class="lazy-tag"', result)
        self.assertIn('class="lazy-tag-spinner-container"', result)

    def test_decorated_tag_with_render_tag_renders_tag(self):
        result = test_tags.test_simple_dec_args(1, kwarg='hello',
                                                render_tag=True)

        self.assertEqual(result, '1 hello')


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

    def test_get_lib_and_tag_name_regular_template_tag(self):
        tag = 'test_lib.test_tag'

        lib, tag_name = get_lib_and_tag_name(tag)

        self.assertEqual(lib, 'test_lib')
        self.assertEqual(tag_name, 'test_tag')

    def test_get_lib_and_tag_name_sub_package(self):
        tag = 'test_lib.sub.test_tag'

        lib, tag_name = get_lib_and_tag_name(tag)

        self.assertEqual(lib, 'test_lib.sub')
        self.assertEqual(tag_name, 'test_tag')

    def test_get_lib_and_tag_name_requires_correct_format(self):
        tag = 'fail'

        with self.assertRaises(ValueError):
            lib, tag_name = get_lib_and_tag_name(tag)
