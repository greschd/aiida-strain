# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Test fixtures providing input for the strain workchains.
"""

# pylint: disable=unused-argument,redefined-outer-name,missing-docstring

import pytest

__all__ = ['strain_kind', 'strain_parameters', 'strain_inputs']


@pytest.fixture(
    params=[
        'three_five.Biaxial001',
        'three_five.Biaxial110',
        'three_five.Biaxial111',
        'three_five.Uniaxial110',
    ]
)
def strain_kind(request):
    return request.param


@pytest.fixture(params=[
    'InAs',
    'InSb',
    'GaSb',
])
def strain_parameters(request):
    return request.param


@pytest.fixture
def strain_inputs(configure, strain_kind, strain_parameters, sample):
    import pymatgen
    from aiida import orm

    structure = orm.StructureData()
    structure.set_pymatgen(pymatgen.Structure.from_file(sample('POSCAR')))

    return dict(
        structure=structure,
        strain_kind=orm.Str(strain_kind),
        strain_parameters=orm.Str(strain_parameters),
        strain_strengths=orm.List(list=[-0.2, -0.1, 0., 0.1, 0.2])
    )
