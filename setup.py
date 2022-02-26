from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="channels_auth_token_middlewares",
    version="1.0.0",
    description="Django Channels auth token middlewares",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YegorDB/django-channels-auth-token-middlewares",
    author="Yegor Bitensky",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="django channels middleware",
    packages=find_packages(exclude=["docs*", "tests*", "tutorial*"]),
    python_requires=">=3.6",
    install_requires=["channels>=3"],
)
