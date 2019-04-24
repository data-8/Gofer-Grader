from setuptools import find_packages, setup

setup(
    name='gofer_grader',
    version='1.1.0',
    license='3-clause BSD',
    author='Vincent Su',
    author_email='vipasu@berkeley.edu',
    description='Lightweight autograder for python files and notebooks',
    packages=find_packages(),
    install_requires=[
        'jinja2',
        'pygments',
        'tornado'
    ]
)
