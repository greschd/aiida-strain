#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Example applying uniaxial 110 strain on InSb, and filtering
the symmetries.
"""

import sys
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)))

from aiida import orm
from aiida.engine.launch import run

from aiida_strain import ApplyStrainsWithSymmetry

from run_strain import get_strain_input

if __name__ == '__main__':
    print(
        run(
            ApplyStrainsWithSymmetry,
            symmetries=orm.SinglefileData(file=abspath('symmetries.hdf5')),
            symmetry_repr_code=orm.Code.get_from_string('symmetry-repr'),
            **get_strain_input()
        )
    )
