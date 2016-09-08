set -e
if [ "$LINT" ]; then
    flake8 *.py parsers gis tests
else
    python setup.py test
fi
