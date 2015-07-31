# Deploys an update to PyPI
python setup.py clean
python setup.py sdist bdist_wheel
twine upload dist/*