from setuptools import setup
from setuptools import find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='ptv-wrapper',
    version='0.1.0',
    packages=find_packages(),
    description='An API Wrapper for Public Transport Victoria (PTV)',
    long_description=readme,
    url='https://github.com/abrizzz/ptv-wrapper',
    license='MIT',
    author='Akshay Brizmohun',
    author_email='aksh1000@gmail.com',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords=['ptv', 'melbourne', 'victoria', 'public transport'],
    install_requires=['requests'],
    tests_require=['pytest'],
)
