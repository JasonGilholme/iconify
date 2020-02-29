
import os

from setuptools import setup, find_packages

import json


githubEventData = os.environ.get('GITHUB_EVENT_PATH')
if githubEventData is not None:
    with open(githubEventData, 'r') as infile:
        data = json.load(infile)

    import pprint
    pprint.pprint(data)


setup(
    name='iconify',
    version='0.0.{}'.format(os.environ.get('GITHUB_RUN_NUMBER', 'dev')),
    description='An SVG based icon library for Qt',
    long_description="",
    long_description_content_type='text/markdown',
    author='Jason Gilholme',
    author_email='jasongilholme@gmail.com',
    license='GPLv3',
    url='https://github.com/jasongilholme/iconify',
    keywords=['Qt', 'icons', 'svg', 'PySide', 'PyQt'],
    packages=find_packages(),
    install_requires=['qtpy', 'six'],
    include_package_data=True,
    platforms=['OS-independent'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: User Interfaces',
    ],
    entry_points={
        'console_scripts': [
            'iconify-browser=iconify.browser:run',
            'iconify-fetch=iconify.fetch:fetch',
            'iconify-fetch-fa=iconify.fetch:fontAwesome',
            'iconify-fetch-mdi=iconify.fetch:materialDesign',
            'iconify-fetch-ei=iconify.fetch:elusiveIcons',
        ],
    }
)
