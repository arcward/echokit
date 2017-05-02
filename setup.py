from setuptools import setup


setup(
    name='echokit',
    version='0.3.0',
    author='Edward Wells',
    author_email='git@edward.sh',
    description="Alexa Skills Kit SDK for Python 3.6",
    license='MIT',
    keywords='Amazon AWS Alexa Skills Kit ASK py3 python3.6 lambda',
    url='https://github.com/arcward/echokit',
    packages=['echokit'],
    entry_points={
        'console_scripts': ['echodist=echokit.echodist:echodist']
    }
)