from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='esports_api',
    version='0.1',
    description='A flask framework for developing quick APIs relating to esports titles.',
    license="GPL3",
    long_description=long_description,
    author='Joe Paton',
    author_email='joantpat@gmail.com',
    url="https://github.com/Jopat2409/esports-api",
    packages=['esports_api'],
    install_requires=['flask', 'python-dotenv', 'lxml', 'requests'], #external packages as dependencies
)
