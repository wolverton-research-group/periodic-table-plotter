from setuptools import setup, find_packages

setup(
    name='periodic-table-plotter',
    version='0.1',
    author='S. Kirklin',
    author_email='scott.kirklin@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/periodic-table-plotter',
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    package_data = {'': ['*.yml', '*.txt']},
    install_requires=[
        'qmpy >= 0.48',
        'numpy',
        'matplotlib'
    ],
)
