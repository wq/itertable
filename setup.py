from setuptools import setup


LONG_DESCRIPTION = """
Iterable API for tabular datasets including CSV, XLSX, XML, & JSON.
"""


def readme():
    try:
        readme = open('README.md')
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()


setup(
    name='itertable',
    use_scm_version=True,
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='https://github.com/wq/itertable',
    license='MIT',
    packages=[
        'itertable',
        'itertable.parsers',
        'itertable.gis',
    ],
    description=LONG_DESCRIPTION.strip(),
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=['requests', 'openpyxl', 'click'],
    extras_require={
        'gis': ['Fiona', 'geopandas'],
        'pandas': ['pandas'],
        'oldexcel': ['xlrd', 'xlwt'],
    },
    setup_requires=[
        'setuptools_scm',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Utilities',
    ],
)
