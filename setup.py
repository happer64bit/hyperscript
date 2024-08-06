from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

long_description = ""
if os.path.exists('README.md'):
    with open('README.md', 'r') as file:
        long_description = file.read()

# Define Cython extension
extensions = [
    Extension(
        name="hyperscript_cli.parser",
        sources=["hyperscript_cli/parser.pyx"],
        extra_compile_args=['/O2']
    )
]

cython_directives = {'embedsignature': True}

setup(
    name='hyperscript-cli',
    version='1.0.4',
    description='Powerful HTTP Request Tester',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Happer',
    author_email='happer64bit@gmail.com',
    url='https://github.com/happer64bit/hyperscript',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyyaml',
        'colorama',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='configuration requests API handling',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'hyperscript=hyperscript_cli.__main__:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    ext_modules=cythonize(extensions, compiler_directives=cython_directives, language_level='3'),
)
