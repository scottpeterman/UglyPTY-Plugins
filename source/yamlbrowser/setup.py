from setuptools import setup, find_packages

setup(
    name="uglyplugin_yamlbrowser",
    version="0.1.0",
    description="Basic TFTP Server Plugin For UglyPTY - A PyQt6-based plugin using Pyserial",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Scott Peterman",
    author_email="scottpeterman@gmail.com",
    url="https://github.com/scottpeterman/UglyPTY",  # Replace with your repository URL
    license="GPL",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['charset-normalizer==3.2.0',
                     'crayons==0.4.0',
                     'cryptography==41.0.1',
                     'darkdetect==0.7.1',
                     'decorator==5.1.1',
                     'executing==1.2.0',
                     'future==0.18.3',
                     'greenlet==2.0.2',
                     'inflection==0.5.1',
                     'jedi==0.19.0',
                     'Jinja2==3.1.2',
                     'MarkupSafe==2.1.3',
                     'matplotlib-inline==0.1.6',
                     'mypy-extensions==1.0.0',
                     'numpy==1.25.2',
                     'paramiko==3.2.0',
                     'pickleshare==0.7.5',
                     'pure-eval==0.2.2',
                     'pycparser==2.21',
                     'pycryptodome==3.18.0',
                     'Pygments==2.16.1',
                     'PyNaCl==1.5.0',
                     'PyQt6==6.5.1',
                     'PyQt6-Qt6==6.5.1',
                     'PyQt6-sip==13.5.1',
                     'PyQt6-WebEngine==6.5.0',
                     'PyQt6-WebEngine-Qt6==6.5.1',
                     'pyqtdarktheme==2.1.0',
                     'pyserial==3.5',
                     'python-dateutil==2.8.2',
                     'python-igraph==0.10.6',
                     'pytz==2023.3',
                     'PyYAML==6.0.1',
                     'qt-material==2.14',
                     'requests==2.31.0',
                     'scp==0.14.5',
                     'six==1.16.0',
                     'stack-data==0.6.2',
                     'svgwrite==1.4.3',
                     'texttable==1.6.7',
                     'tomli==2.0.1',
                     'traitlets==5.9.0',
                     'typing-inspect==0.9.0',
                     'typing_extensions==4.7.1',
                     'tzdata==2023.3',
                     'urllib3==2.0.4',
 'wcwidth==0.2.6'],
    #
    #
# scripts=['uglypty/uglypty.py'],
    package_data={
        'uglyplugin_yamlbrowser': [

            'uglyplugin_yamlbrowser/*',


        ],
    },
    python_requires='>=3.9',
)
