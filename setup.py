from setuptools import setup, find_packages

setup(
    name='hyperscript-cli',
    version='1.0',
    description='Powerful HTTP Request Tester',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Happer',
    author_email='happer64bit@gmail.com',
    url='https://github.com/happer64bit/hyperscript',  # URL to the project repository
    packages=find_packages(),
    install_requires=[
        'requests',  # Fixed typo
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
)
