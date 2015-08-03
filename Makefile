export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH=.

.PHONY: test

test:
	coverage run --source=lazy_tags `which django-admin.py` test tests
	coverage report

publish:
	python setup.py clean
	python setup.py sdist bdist_wheel
	twine upload dist/*

runserver:
	`which django-admin.py` runserver