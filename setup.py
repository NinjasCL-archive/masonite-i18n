from setuptools import setup

setup(
    name="Masonite i18n",
    version='0.0.1',
    packages=['locale'],
    license='MIT',
    author='Camilo Castro',
    author_email='camilo@ninjas.cl',
    description='Provides i18n to Masonite',
    url='http://ninjas.cl',
    install_requires=[
        'masonite',
    ],
    include_package_data=True,
)
