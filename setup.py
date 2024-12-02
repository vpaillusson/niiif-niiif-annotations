from setuptools import setup, find_packages

def read_file(file):
   with open(file) as f:
        return f.read()
   
setup(
    name='Manifest IIIF by EFEO',
    version='v1.1.0',
    description='Manage IIIF manifest',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author=['EFEO', 'Humanum'],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
        'argparse',
        'tqdm',
        'pandas'
        ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
    ],
    license="WTFPL",
    intended_audience=['Developers', 'Science/Research'],
)