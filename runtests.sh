set -e
if [ "$LINT" ]; then
    flake8 setup.py itertable tests
else
    python setup.py test
fi
