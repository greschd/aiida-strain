#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

"""
Usage: python configure.py config_input_file config_output_file
"""

import sys
import subprocess
from os.path import join


def get_path(codename):
    return subprocess.check_output(
        'which {}'.format(codename), shell=True).decode().strip()


symmetry_repr_path = get_path('symmetry-repr')

with open(sys.argv[1], 'r') as f:
    res = f.read().format(symmetry_repr_path=symmetry_repr_path)
with open(sys.argv[2], 'w') as f:
    f.write(res)
