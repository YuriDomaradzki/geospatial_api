from setuptools import setup, find_packages

VERSION = '0.1.0' 
DESCRIPTION = 'Implementation of a private REST API for geospatial data'
LONG_DESCRIPTION = "This package provides an implementation of a REST API for geospatial data."

with open('requirements.txt', 'r') as reqs:
    requires = [req.replace('\n', '') for req in reqs.readlines()]

packages = find_packages()

setup(
        name="geospatial_api", 
        version=VERSION,
        author="Yuri Domaradzki",
        author_email="yuridomaradzki@gmail.com",
        url="https://github.com/YuriDomaradzki/geospatial_api.git",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license='MIT',
        keywords='geospatial data REST API',
        packages=packages,
        include_package_data=True,
        install_requires=requires,
        classifiers= [
            "Development Status :: 1 - Planning",
            'Programming Language :: Python :: 3 :: Only',
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ]
)