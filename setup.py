
import os
from setuptools import setup, find_packages

version = 'dev'

dir_ = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(dir_, 'README.md')) as f:
    long_description = f.read()

setup(
    name='iconify',
    version=version,
    description="An icon and image library for Qt that lets you use svg's "
                "from common packs like FontAwesome, MateriallDesign etc.",
    long_description=long_description,
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
            'iconify-fetch-dash=iconify.fetch:dashIcons',
            'iconify-fetch-feather=iconify.fetch:featherIcons',
            'iconify-fetch-google-emojis=iconify.fetch:googleEmojis',
        ],
    }
)
