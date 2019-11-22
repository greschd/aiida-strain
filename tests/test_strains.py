# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the ApplyStrains workchain.
"""

from strain_inputs import *  # pylint: disable=unused-wildcard-import


def test_strains(
    configure_with_daemon,  # pylint: disable=unused-argument
    strain_inputs  # pylint: disable=redefined-outer-name
):
    """
    Basic test running the ApplyStrains workchain.
    """
    from aiida.engine import run
    from aiida.plugins import DataFactory
    from aiida_strain import ApplyStrains

    inputs = strain_inputs
    strain_list = inputs['strain_strengths'].get_attribute('list')

    result = run(ApplyStrains, **strain_inputs)

    for strain_val in strain_list:
        key = 'structure_{}'.format(strain_val).replace('.', '_dot_').replace('-', '_m_')
        assert key in result
        assert isinstance(result[key], DataFactory('structure'))
