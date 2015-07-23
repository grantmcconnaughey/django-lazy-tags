# django-lazy-tags

## Installation

1\. Install via pip

```python
pip install django-lazy-tags
```

2\. Add to installed apps

```python
INSTALLED_APPS = (
    # ...
    'lazy_tags',
)
```

3\. Add the lazy tags urls to your root urlconf.

```python
urlpatterns = patterns('',
    # ...
    url(r'^lazy_tags/', include('lazy_tags.urls')),
)
```

## Usage

First, load the `lazy_tags` library in your templates.

    {% load lazy_tags %}

Then, call the `lazy_tag` template tag passing your tag name as the first parameter. The format is `tag_library.tag_name` where `tag_library` is what you would load at the top of the page (e.g. `my_tags`) and `tag_name` is the name of your template tag (e.g. `my_template_tag`). After the first argument to `lazy_tag` simply pass the rest of the args and kwargs just as you would pass them to your own tag.

This:

    {% load my_tags %}

    {% my_template_tag arg1 arg2 kw1='hello' kw2='world' %}

Becomes this:

    {% load lazy_tags %}

    {% lazy_tag 'my_tags.my_template_tag' arg1 arg2 kw1='hello' kw2='world' %}


## Customizing the Loading Animation

This is the default HTML on the page before the AJAX request completes:

    <div id="{id}" class="lazy-tag-replace">
        <div class="lazy-tag-spinner-container"
             style="width: 100%; text-align: center;">
            <img id="{id}-spinner" class="lazy-tag-spinner"
                 style="width: 15px; height: 15px;"
                 src="{static_url}img/lazy_tags/spinner.gif" />
        </div>
    </div>

To customize the loading animation, override the `lazy-tag-replace`, `lazy-tag-spinner-container`, or `lazy-tag-spinner` classes in your CSS.


## Current Limitations

* jQuery required for the the AJAX calls
* Does not work with tags that take context
* Template tag arguments must be serializable
* Template tag arguments are always strings
