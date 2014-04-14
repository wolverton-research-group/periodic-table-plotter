from setuptools import setup, find_packages

setup(
    name='periodic-table-plotter',
    version='0.2',
    author='S. Kirklin',
    author_email='scott.kirklin@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/periodic-table-plotter',
    license='LICENSE',
    package_data = {'': ['*.yml', '*.md']},
    install_requires=[
        'numpy',
        'matplotlib'
    ],
)
