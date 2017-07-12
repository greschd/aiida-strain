#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiida.orm import DataFactory
from aiida.orm.data.base import List, Str
from plum.util import load_class
from aiida.work.workchain import WorkChain

class ApplyStrains(WorkChain):
    @classmethod
    def define(cls, spec):
        super(ApplyStrain, cls).define(spec)

        spec.input('structure', valid_type=DataFactory('structure'))
        spec.input('strain_kind', valid_type=Str)
        spec.input('strain_parameters', valid_type=Str)
        spec.input('strain_strengths', valid_type=List)

        spec.outline(cls.apply_strain)

    def apply_strain(self):
        strain_classname = 'strain.structure.' + self.inputs.strain_kind.value
        strain_class = load_class(strain_classname)

        strain_parametername = 'strain.parameter.' + self.inputs.strain_parameters.value
        strain_parameters = load_class(strain_parametername)

        strain_instance = strain_class(**strain_parameters)

        structure = self.inputs.structure.to_pymatgen()

        for strength_value in self.inputs.strain_strengths:
            new_structure = strain_instance.apply(structure, strength_multiplier=strength_value)
            new_structure_data = DataFactory('structure')()
            new_structure_data.set_pymatgen(new_structure)
            self.out('strain_{}'.format(strength_value), new_structure_data)
