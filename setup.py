"""``CloudSelect`` lives on `GitHub <https://github.com/ezh/cloudselect>`_."""
# read the contents of your README file
from os import path

from setuptools import find_packages, setup

__version__ = "20.1.6"


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cloudselect",
    author="Alexey Aksenov",
    author_email="ezh@ezh.msk.ru",
    package_data={"cloudselect": ["cloud.json.dist"]},
    description="FZF selector for cloud instances",
    download_url="https://github.com/ezh/cloudselect/archive/v_01.tar.gz",
    entry_points={
        "console_scripts": [
            "cloudselect=cloudselect.cloudselect:main",
            "cloudselect_completer=cloudselect.cloudselect:complete",
        ],
    },
    install_requires=[
        "appdirs==1.4.3",
        "boto3==1.11.14",
        "chardet==3.0.4",
        "dependency-injector==3.15.4",
        "pyyaml==5.2",
    ],
    include_package_data=True,
    keywords=["Cloud", "CLI", "FZF", "SSH", "SCP", "AWS"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3",
    url="https://github.com/ezh/cloudselect",
    version=__version__,
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Shells",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
