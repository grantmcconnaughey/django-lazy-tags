export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH=.

.PHONY: test

test:
	coverage run --source=lazy_tags `which django-admin.py` test tests
	coverage report

publish: clean
	python setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -vrf ./build ./dist ./*.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.tgz' -delete

runserver:
	`which django-admin.py` runserver