from setuptools import setup, find_packages

setup(
    name="blogify",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-dotenv',
        'requests',
        'sqlalchemy',
    ],
) 