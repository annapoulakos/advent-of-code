from setuptools import setup
import functools
import pathlib

def read(*path):
    target = functools.reduce(lambda a,b: a/b, path, pathlib.Path(__file__).parent)
    with target.open(mode='r') as handle:
        return handle.read()

about = {}
exec(read('core', '__version__.py'), about)

setup(
    name=about['__title__'],
    author=about['__author__'],
    description=about['__description__'],
    version=about['__version__'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license=read('LICENSE'),
    install_required=[
        'Click==7.0',
        'numpy==1.15.4',
    ],
    entry_points={
        'console_scripts': [
            'aoc=core.aoc:cli',
        ]
    }
)
