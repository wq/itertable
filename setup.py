from os.path import join, dirname
from setuptools import setup, find_packages

LONG_DESCRIPION = """
Consistent API for reading and writing to external datasets
"""

def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION

setup(
    name = 'wq.io',
    version = '0.4.0-dev',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='http://wq.io/wq.io',
    license='MIT',
    packages=find_packages(),
    namespace_packages=['wq'],
    description='Consistent iterable API for reading and writing to external datasets',
    long_description=long_description(),
    install_requires=['httplib2','lxml','xlrd'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Scientific/Engineering :: GIS',
    ]
)
