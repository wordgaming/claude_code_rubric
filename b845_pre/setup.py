from setuptools import setup, find_packages

# Read README with UTF-8 encoding to handle special characters
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='field-calc',
    version='old.0.0',
    description='Multi-charge electric field and potential calculator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Physics Calculator Team',
    author_email='physics@example.com',
    url='https://github.com/example/field-calc',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'field-calc=field_calc.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords='electric field potential charge physics coulomb',
)
