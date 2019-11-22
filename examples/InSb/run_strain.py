#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Example applying uniaxial 110 strain to InSb.
"""

import pymatgen

from aiida.orm.nodes.data.str import Str
from aiida.orm.nodes.data.list import List
from aiida.orm import StructureData
from aiida.engine.launch import run

from aiida_strain import ApplyStrains


def get_strain_input(  # pylint: disable=missing-docstring
    strain_kind='three_five.Uniaxial110',
    strain_parameters='InSb',
    strain_strengths=(-0.02, -0.01, 0.01, 0.02)
):
    structure = StructureData()
    structure.set_pymatgen(pymatgen.Structure.from_file('POSCAR'))

    return dict(
        structure=structure,
        strain_kind=Str(strain_kind),
        strain_parameters=Str(strain_parameters),
        strain_strengths=List(list=strain_strengths)
    )


if __name__ == '__main__':
    print(run(ApplyStrains, **get_strain_input()))
