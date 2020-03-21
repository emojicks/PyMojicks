from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('pymojicks/__init__.py') as f:
    version = re.search(r"__version__ = '(.+)'", f.read()).group(1)

readme = ''
with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='pymojicks',
    author='NCPlayz',
    url='https://github.com/emojicks/PyMojicks',
    project_urls={
        'Issue tracker': 'https://github.com/emojicks/PyMojicks/issues'
    },
    version=version,
    packages=['pymojicks'],
    description='The Official Emojicks Interpreter for Python.',
    long_description=readme
)
