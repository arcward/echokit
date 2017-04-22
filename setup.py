from setuptools import setup


setup(
    name='echopy',
    version='0.1.1',
    author='Edward Wells',
    author_email='git@edward.sh',
    description="Alexa Skills Kit SDK for Python 3.6",
    license='MIT',
    keywords='Amazon AWS Alexa Skills Kit ASK py3 python3.6 lambda',
    url='https://github.com/arcward/echopy',
    packages=['echopy'],
    entry_points={
        'console_scripts': ['echodist=echopy.cli:echodist']
    }
)