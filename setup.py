import os
from setuptools import setup, find_packages


LONG_DESCRIPTION = """
Consistent iterable API for reading and writing to external datasets
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    # Attempt to run pandoc on markdown file
    import subprocess
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open(os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        ))
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()


def get_version():
    version = open("version.py").read().strip()
    version = version.replace("VERSION = ", '')
    version = version.replace('"', '')
    return version


def create_wq_namespace():
    """
    Generate the wq namespace package
    (not checked in, as it technically is the parent of this folder)
    """
    if os.path.isdir("wq"):
        return
    os.makedirs("wq")
    init = open(os.path.join("wq", "__init__.py"), 'w')
    init.write("__import__('pkg_resources').declare_namespace(__name__)")
    init.close()


def find_wq_packages(submodule):
    """
    Add submodule prefix to found packages.  The packages within each wq
    submodule exist at the top level of their respective repositories.
    """
    packages = ['wq', submodule]
    package_dir = {submodule: '.'}
    for package in find_packages():
        if package == 'wq':
            continue
        full_name = submodule + "." + package
        packages.append(full_name)
        package_dir[full_name] = package.replace('.', os.sep)

    return packages, package_dir


create_wq_namespace()
packages, package_dir = find_wq_packages('wq.io')


setup(
    name='wq.io',
    version=get_version(),
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='http://wq.io/wq.io',
    license='MIT',
    packages=packages,
    package_dir=package_dir,
    namespace_packages=['wq'],
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    install_requires=['httplib2', 'xlrd'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Scientific/Engineering :: GIS',
    ]
)
