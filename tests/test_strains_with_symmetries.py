# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import pytest

from strain_inputs import *


def test_strains(configure_with_daemon, strain_inputs, sample):
    from aiida.engine import run
    from aiida.plugins import DataFactory
    from aiida.orm import Code
    from aiida_strain.work import ApplyStrainsWithSymmetry

    inputs = strain_inputs
    strain_list = inputs['strain_strengths'].get_attr('list')

    result = run(
        ApplyStrainsWithSymmetry,
        symmetries=DataFactory('singlefile')(file=sample('symmetries.hdf5')),
        symmetry_repr_code=Code.get_from_string('symmetry_repr'),
        **inputs)

    for s in strain_list:
        structure_key = 'structure_{}'.format(s).replace('.', '_dot_')
        assert structure_key in result
        assert isinstance(result[structure_key], DataFactory('structure'))
        symmetries_key = 'symmetries_{}'.format(s).replace('.', '_dot_')
        assert symmetries_key in result
        assert isinstance(result[symmetries_key], DataFactory('singlefile'))
    for key in result:
        key_withdot = key.replace('_dot_', '.')
        assert len(key_withdot.split('_')) <= 2
