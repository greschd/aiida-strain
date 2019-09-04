# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import pytest

from strain_inputs import *


def test_strains(configure_with_daemon, strain_inputs):
    from aiida.engine import run
    from aiida.plugins import DataFactory
    from aiida_strain.work import ApplyStrains

    inputs = strain_inputs
    strain_list = inputs['strain_strengths'].get_attr('list')

    result = run(ApplyStrains, **strain_inputs)

    for s in strain_list:
        key = 'structure_{}'.format(s).replace('.', '_dot_')
        assert key in result
        assert isinstance(result[key], DataFactory('structure'))
