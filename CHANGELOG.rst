Changelog
=========

* 0.4.0 (December 2, 2015)
    * Added Python 3.5 support
    * Added Django 1.9 support
    * Removed Python 2.6 support
    * Removed Django 1.4, 1.5, and 1.6 support

* 0.3.1 (August 9, 2015)
    * Works with template tags in subpackages, e.g. {% load foo.bar %}

* 0.3.0 (August 3, 2015)
    * Add lazy_tag decorator.
    * Added setting to use jQuery, Prototype, or pure JavaScript for AJAX

* 0.2.1-0.2.3 (July 31, 2015)
    * Fixed MANIFEST.in [#]_

* 0.2.0 (July 30, 2015)
    * Use Django cache instead of URL parameters in order to prevent potential remote code execution.
    * Fixed issue where tags with multiple args would not work.
    * Removed template tag args/kwargs always being passed in as strings.
    * Removed LAZY_TAGS_FORCE_LOGIN setting. Not needed now that remote code execution issue is fixed.

* 0.1 (July 28, 2015)
    * Initial alpha release

.. [#] `"Every Python project has a "Fix MANIFEST.in" commit. Look it up, it’s true." <https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/>`_