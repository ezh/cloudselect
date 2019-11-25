from setuptools import find_packages, setup

import cloudselect

setup(
    name="cloudselect",
    author="Alexey Aksenov",
    author_email="ezh@ezh.msk.ru",
    data_files={"cloudselect": ["cloud.json.dist"]},
    description="FZF selector for cloud instances",
    download_url="https://github.com/ezh/cloudselect/archive/v_01.tar.gz",
    entry_points={"console_scripts": ["cloudselect=cloudselect.cloudselect:main"]},
    install_requires=["boto3", "dependency_injector"],
    keywords=["AWS", "CLI", "FZF", "SSH", "SCP"],
    license="MIT",
    packages=find_packages(include=["cloudselect"]),
    python_requires=">=3",
    url="https://github.com/ezh/cloudselect",
    version=cloudselect.__version__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
