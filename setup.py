from setuptools import setup, find_packages

setup(
    name='portstat',
    version='0.0.1',
    keywords= ('port', 'monitor', 'traffic'),
    url='https://github.com/imlonghao/portstat',
    license='Apache License 2.0',
    author='imlonghao',
    author_email='shield@fastmail.com',
    description='A simple port traffic monitor',
    packages=find_packages(),
    platforms='any',
    entry_points={
        'console_scripts': [
            'portstat=portstat.portstat:main'
        ]
    }
)
