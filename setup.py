# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import re
from setuptools import setup, find_packages

# Get the version number
with open('./aiida_strain/__init__.py') as f:
    match_expr = "__version__[^'\"]+(['\"])([^'\"]+)"
    version = re.search(match_expr, f.read()).group(2).strip()

if __name__ == '__main__':
    setup(
        name='aiida-strain',
        version=version,
        description='AiiDA Plugin for applying strain to structures',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        url='https://aiida-strain.readthedocs.io',
        license='Apache 2.0',
        classifiers=[
            'Development Status :: 3 - Alpha', 'Environment :: Plugins',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='strain aiida workflows',
        packages=find_packages(exclude=['aiida']),
        include_package_data=True,
        setup_requires=['reentry'],
        reentry_register=True,
        install_requires=[
            'aiida-core', 'strain', 'aiida-symmetry-representation',
            'aiida-tools'
        ],
        extras_require={
            'test': ['aiida-pytest', 'pytest'],
            'pre-commit': ['pre-commit', 'yapf==0.25']
        },
        entry_points={},
    )
