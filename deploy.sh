# Deploys an update to PyPI
python setup.py clean
python setup.py bdist_wheel
twine upload dist/*