from setuptools import setup
from locale import VERSION

setup(
    name='Masonite i18n',
    version=VERSION,
    packages=['locale'],
    license='MIT',
    author='Camilo Castro',
    author_email='camilo@ninjas.cl',
    description='Provides i18n to Masonite',
    url='http://ninjas.cl',
    install_requires=[
        'masonite',
    ],
    keywords=['i18n', 'translation', 'python3', 'masonite'],
    include_package_data=True,
)
