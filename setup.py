from setuptools import setup, find_packages

setup(
    name="application_review_system",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'application_review_system': ['templates/*'],
    },
    install_requires=[
        'Flask>=2.0.1',
        'pandas>=1.3.3',
        'openpyxl>=3.0.9',
    ],
    entry_points={
        'console_scripts': [
            'application-review=application_review_system.app:main',
        ],
    },
)