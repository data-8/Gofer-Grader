from setuptools import find_packages, setup

setup(
    name='gradememaybe',
    version='0.6',
    license='3-clause BSD',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    description='Simple alternative to okpy for grading only',
    packages=find_packages(),
    install_requires=[
        'jinja2',
        'pygments'
    ]
)
