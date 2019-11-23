from setuptools import setup, find_packages
import awselect

setup(
    name='awselect',
    author='Alexey Aksenov',
    author_email='ezh@ezh.msk.ru',
    description='AWS FZF selector for AWS instances',
    download_url='https://github.com/ezh/awssh/archive/v_01.tar.gz',
    entry_points={
        'console_scripts': [
            'awselect=awselect.cli:main',
        ],
    },
    keywords=['AWS', 'CLI', 'FZF', 'SSH', 'SCP'],
    license='MIT',
    packages=find_packages(include=['awselect']),
    python_requires='>=3',
    url='https://github.com/ezh/awselect',
    version=awselect.__version__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
