from setuptools import setup, find_packages

setup(
    name='tgi',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'start-tgi=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['config.json'],
    },
)
