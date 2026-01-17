from setuptools import setup, find_packages

setup(
    name="sicat",
    version="1.0.0",
    description="Advanced Vulnerability & Exploit Scanner",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Justakazh",
    url="https://github.com/justakazh/sicat",
    
    # Pack up the 'lib' and 'sources' directories
    packages=find_packages(),
    
    # Pack up the 'sicat.py' file as a module
    py_modules=['sicat'],
    
    include_package_data=True,
    install_requires=[
        "colorama>=0.4.6",
        "Flask>=3.1.2",
        "requests>=2.32.5",
        "webtech>=1.3.4",
    ],
    entry_points={
        'console_scripts': [
            'sicat=sicat:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
