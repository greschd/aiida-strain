# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='aiida-strain',
        version='0.0.0a1',
        description='AiiDA Plugin for applying strain to structures',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        license='GPL',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Plugins',
            'Framework :: AiiDA',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='strain aiida workflows',
        packages=find_packages(exclude=['aiida']),
        include_package_data=True,
        setup_requires=[
            'reentry'
        ],
        reentry_register=True,
        install_requires=[
            'aiida-core', 'strain', 'plum'
        ],
        extras_require={'test': ['aiida-pytest', 'pytest']},
        entry_points={},
    )
