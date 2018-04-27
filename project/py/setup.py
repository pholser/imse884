from setuptools import setup, find_packages

setup(
    name='vertex-coloring',
    version='1.0.0',
    description='IP solver for vertex coloring problem in graphs',
    author='Paul Holser',
    author_email='pholser@ksu.edu',
    packages=find_packages(),
    install_requires=[
        'networkx>=2.1',
        'matplotlib>=2.2.2',
        'pytest>=3.5.0'
    ]
)
