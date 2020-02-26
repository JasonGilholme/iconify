
from setuptools import setup, find_packages


setup(
    name='iconify',
    version='0.0.0.dev',
    url='https://github.com/jasongilholme/iconify.git',
    author='Jason Gilholme',
    author_email='jasongilholme@gmail.com',
    description='',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'iconify-browser=iconify.browser:run',
            'iconify-fetch-fontawesome=iconify.fetch:fontAwesome',
        ],
    }
)
