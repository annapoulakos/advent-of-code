from setuptools import setup, find_packages

setup(
    name='ap-aoc-2020',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'aoc=app.cli:cli',
        ]
    }
)
