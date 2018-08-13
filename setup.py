from setuptools import setup, find_packages
from lang import VERSION

setup(
    name='masonite-i18n',
    version=VERSION,
    packages=find_packages(),
    license='MIT',
    author='Camilo Castro',
    author_email='camilo@ninjas.cl',
    description='Provides i18n to Masonite',
    url='https://github.com/clsource/masonite-i18n',
    install_requires=[
        'hjson',
    ],
    keywords=['i18n', 'translation', 'python3', 'masonite'],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
