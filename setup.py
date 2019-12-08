"""``CloudSelect`` lives on `GitHub <https://github.com/ezh/cloudselect>`_."""
from setuptools import find_packages, setup

__version__ = "19.1"

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
    install_requires=["appdirs", "boto3", "chardet", "dependency_injector"],
    keywords=["Cloud", "CLI", "FZF", "SSH", "SCP", "AWS"],
    license="MIT",
    include_package_data=True,
    packages=find_packages(include=["cloudselect"]),
    python_requires=">=3",
    url="https://github.com/ezh/cloudselect",
    version=__version__,
    classifiers=[
        "Development Status :: 3 - Beta",
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
