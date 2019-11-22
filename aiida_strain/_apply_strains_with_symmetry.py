# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines a workchain for applying strain to a structure, and filter
symmetries that conform to the strained structure.
"""

from aiida import orm
from aiida.engine import WorkChain, ToContext
from aiida_tools import check_workchain_step

from aiida_symmetry_representation.calculations.filter_symmetries import FilterSymmetriesCalculation

from ._apply_strains import ApplyStrains
from ._util import get_structure_key, get_symmetries_key


class ApplyStrainsWithSymmetry(WorkChain):
    """
    Workchain to create strained structures from an input structure, and select the symmetries which are compatible with the strained structure from a set of given input symmetries.
    """
    @classmethod
    def define(cls, spec):
        super(ApplyStrainsWithSymmetry, cls).define(spec)

        spec.expose_inputs(ApplyStrains)
        spec.input('symmetries', valid_type=orm.SinglefileData)
        spec.input('symmetry_repr_code', valid_type=orm.Code)

        spec.outputs.dynamic = True

        spec.outline(cls.run_apply_strain, cls.run_filter_symmetries, cls.finalize)

    @check_workchain_step
    def run_apply_strain(self):
        self.report('Submitting ApplyStrains workchain.')
        return ToContext(
            apply_strains=self.submit(ApplyStrains, **self.exposed_inputs(ApplyStrains))
        )

    @check_workchain_step
    def run_filter_symmetries(self):
        """
        Run the FilterSymmetriesCalculation for each of the
        created strained structures.
        """
        self.report('Running FilterSymmetriesCalculation.')
        apply_strains_outputs = self.ctx.apply_strains.outputs
        apply_strains_output_keys = list(apply_strains_outputs)
        self.report(apply_strains_output_keys)
        tocontext_kwargs = dict()
        for strain_value in self.inputs.strain_strengths:
            builder = FilterSymmetriesCalculation.get_builder()
            structure_key = get_structure_key(strain_value)
            structure_result = apply_strains_outputs[structure_key]
            self.out(structure_key, structure_result)
            symmetries_key = get_symmetries_key(strain_value)

            # inputs = process.get_inputs_template()
            builder.code = self.inputs.symmetry_repr_code
            builder.structure = structure_result
            builder.symmetries = self.inputs.symmetries
            builder.metadata.options = dict(
                resources={
                    'num_machines': 1,
                    'tot_num_mpiprocs': 1
                }, withmpi=False
            )
            tocontext_kwargs[symmetries_key] = self.submit(builder)
        return ToContext(**tocontext_kwargs)

    @check_workchain_step
    def finalize(self):
        """
        Retrieve filtered symmetries.
        """
        self.report('Adding filtered symmetries to outputs.')
        for strain_value in self.inputs.strain_strengths:
            symmetries_key = get_symmetries_key(strain_value)
            self.out(symmetries_key, self.ctx[symmetries_key].outputs.symmetries)
