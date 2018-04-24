#!/usr/bin/env runaiida

import pymatgen

from aiida.orm.data.str import Str
from aiida.orm.data.list import List
from aiida.orm.data.structure import StructureData
from aiida.work.launch import run

from aiida_strain.work import ApplyStrains

def get_strain_input(
    strain_kind='three_five.Uniaxial110',
    strain_parameters='InSb',
    strain_strengths=[-0.02, -0.01, 0.01, 0.02]
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
    result = run(ApplyStrains, **get_strain_input())
    print(result)
