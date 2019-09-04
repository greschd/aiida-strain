#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import os

from aiida.engine.launch import run
from aiida.orm import Code
from aiida.orm import SinglefileData

from aiida_strain.work import ApplyStrainsWithSymmetry

from run_strain import get_strain_input

if __name__ == '__main__':
    result = run(
        ApplyStrainsWithSymmetry,
        symmetries=SinglefileData(file=os.path.abspath('symmetries.hdf5')),
        symmetry_repr_code=Code.get_from_string('symmetry-repr'),
        **get_strain_input())
    print(result)
