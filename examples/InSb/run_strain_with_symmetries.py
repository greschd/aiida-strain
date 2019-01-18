#!/usr/bin/env runaiida

import os

from aiida.work.launch import run
from aiida.orm.code import Code
from aiida.orm.data.singlefile import SinglefileData

from aiida_strain.work import ApplyStrainsWithSymmetry

from run_strain import get_strain_input

if __name__ == '__main__':
    result = run(
        ApplyStrainsWithSymmetry,
        symmetries=SinglefileData(file=os.path.abspath('symmetries.hdf5')),
        symmetry_repr_code=Code.get_from_string('symmetry-repr'),
        **get_strain_input())
    print(result)
