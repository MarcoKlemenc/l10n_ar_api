from setuptools import setup, find_packages
from codecs import open
from os import path

setup(
    name='l10n_ar_api',
    version='1.1.2',
    description='Libreria para localizacion Argentina',
    long_description='Libreria para localizacion Argentina',
    url='https://github.com/odoo-arg/l10n_ar_api',
    author='OPENPYME SRL',
    author_email='dcrocco@openpyme.com.ar',
    license='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='Libreria para localizacion Argentina',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'zeep',
        'python-dateutil',
        'M2Crypto',
        'pytz',
        'unidecode',
        'BeautifulSoup'
    ],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
