from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='itch-framework',
    version='0.0.1',

    description='A Scratch-like environment for python',
    long_description=long_description,
    url='https://github.com/danjpgriffin/itch',
    author='Dan Griffin',
    author_email='itch-framework@xiragon.com',
    license='GPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3.6',
    ],

    keywords='scratch education children',

    packages=['itch'],

    install_requires=['greenlet>=0.4',
                      'pygame>=1.9']

)

