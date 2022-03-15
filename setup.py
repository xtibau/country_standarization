from setuptools import setup, find_packages
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



setup(
    name='country_standarization',
    version='0.1',
    packages=find_packages(),
    url='',
    license='MIT',
    author='Xavier-Andoni Tibau',
    author_email='xavitibau@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
)

