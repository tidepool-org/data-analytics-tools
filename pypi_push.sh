##STOP - Make sure you updated the version in the setup.py to match the version in github to be uploaded.
rm dist/*
rm build/*
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel

python3 -m pip install --user --upgrade twine
##python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
