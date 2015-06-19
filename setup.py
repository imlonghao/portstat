from setuptools import setup, find_packages
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='portstat',
    version='0.0.3',
    keywords=('port', 'monitor', 'traffic'),
    url='https://github.com/imlonghao/portstat',
    license='Apache License 2.0',
    author='imlonghao',
    author_email='shield@fastmail.com',
    description='A simple port traffic monitor',
    long_description=long_description,
    packages=find_packages(),
    platforms='any',
    entry_points={
        'console_scripts': [
            'portstat=portstat.portstat:main'
        ]
    }
)
