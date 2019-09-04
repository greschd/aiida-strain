# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from aiida.plugins import DataFactory
from aiida.orm import List, Str, Float
from aiida.engine import WorkChain
from aiida.common.utils import get_object_from_string
from aiida_tools import check_workchain_step

from .util import get_structure_key

from aiida.engine import calcfunction


class ApplyStrains(WorkChain):
    """
    Workchain to create strained structures from a given input structure.
    """

    @classmethod
    def define(cls, spec):
        super(ApplyStrains, cls).define(spec)

        spec.input('structure', valid_type=DataFactory('structure'))
        spec.input('strain_kind', valid_type=Str)
        spec.input('strain_parameters', valid_type=Str)
        spec.input('strain_strengths', valid_type=List)

        spec.outputs.dynamic = True
        spec.outline(cls.apply_strain)

    @check_workchain_step
    def apply_strain(self):
        for strength_value in self.inputs.strain_strengths:
            self.report(
                'Creating structure for strain {}'.format(strength_value))
            new_structure_data = _apply_single_strain(
                structure=self.inputs.structure,
                strain_kind=self.inputs.strain_kind,
                strain_parameters=self.inputs.strain_parameters,
                strength_value=Float(strength_value))
            self.out(get_structure_key(strength_value), new_structure_data)


@calcfunction
def _apply_single_strain(structure, strain_kind, strain_parameters,
                         strength_value):
    strain_classname = 'strain.structure.' + strain_kind.value
    strain_class = get_object_from_string(strain_classname)

    strain_parametername = 'strain.parameter.' + strain_parameters.value
    strain_parameters = get_object_from_string(strain_parametername)

    strain_instance = strain_class(**strain_parameters)

    pmg_structure = structure.get_pymatgen_structure()
    new_pmg_structure = strain_instance.apply(pmg_structure,
                                              strength_value.value)
    new_structure_data = DataFactory('structure')()
    new_structure_data.set_pymatgen(new_pmg_structure)
    return new_structure_data