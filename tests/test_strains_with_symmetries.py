# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the ApplyStrainsWithSymmetries workchain.
"""

# pylint: disable=unused-argument,redefined-outer-name

from strain_inputs import *  # pylint: disable=unused-wildcard-import


def test_strains(configure_with_daemon, strain_inputs, sample):
    """
    Basic test for the ApplyStrainsWithSymmetries workchain.
    """
    from aiida.engine import run
    from aiida import orm
    from aiida_strain import ApplyStrainsWithSymmetry

    inputs = strain_inputs
    strain_list = inputs['strain_strengths'].get_attribute('list')

    result = run(
        ApplyStrainsWithSymmetry,
        symmetries=orm.SinglefileData(file=sample('symmetries.hdf5')),
        symmetry_repr_code=orm.Code.get_from_string('symmetry_repr'),
        **inputs
    )

    for strain_val in strain_list:
        structure_key = (
            'structure_{}'.format(strain_val).replace('.', '_dot_').replace('-', '_m_')
        )
        assert structure_key in result
        assert isinstance(result[structure_key], orm.StructureData)
        symmetries_key = (
            'symmetries_{}'.format(strain_val).replace('.', '_dot_').replace('-', '_m_')
        )
        assert symmetries_key in result
        assert isinstance(result[symmetries_key], orm.SinglefileData)
    for key in result:
        key_unescaped = key.replace('_dot_', '.').replace('_m_', '-')
        assert len(key_unescaped.split('_')) <= 2
