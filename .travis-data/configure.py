#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Usage: python configure.py config_input_file config_output_file
"""

import sys
import subprocess


def get_path(codename):
    return subprocess.check_output('which {}'.format(codename), shell=True).decode().strip()


SYMMETRY_REPR_PATH = get_path('symmetry-repr')

with open(sys.argv[1], 'r') as f:
    CONFIG = f.read().format(symmetry_repr_path=SYMMETRY_REPR_PATH)
with open(sys.argv[2], 'w') as f:
    f.write(CONFIG)
