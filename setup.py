"""Subtitle downloader."""


from setuptools import setup


setup(
    name='subtitle-downloader',
    version='0.1.0',
    packages=['subtitle-downloader'],
    include_package_data=True,
    install_requires=[
        "beautifulsoup4==4.6.0",
        "bs4==0.0.1",
        "certifi==2017.4.17",
        "chardet==3.0.3",
        "click==6.7",
        "idna==2.5",
        "lxml==3.8.0",
        "requests==2.20.0",
        "sh==1.12.14",
        "urllib3==1.26.5"
    ]
)
