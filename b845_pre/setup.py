# setup.py
from setuptools import setup, find_packages

setup(
    name='field-calc',
    version='0.old.0',
    packages=find_packages(),     
    entry_points={'console_scripts': [
        'field-calc=field_calc.cli:main',
        ]},
    install_requires=['sympy'],
    python_requires='>=3.6',
)
