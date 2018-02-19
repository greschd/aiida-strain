from aiida.orm import DataFactory
from aiida.orm.code import Code
from aiida.work import submit
from aiida.work.workchain import WorkChain, ToContext
from aiida_tools import check_workchain_step

from aiida_symmetry_representation.calculations.filter_symmetries import FilterSymmetriesCalculation
from . import ApplyStrains
from ._util import _get_structure_key, _get_symmetries_key

class ApplyStrainsWithSymmetry(WorkChain):
    @classmethod
    def define(cls, spec):
        super(ApplyStrainsWithSymmetry, cls).define(spec)

        spec.expose_inputs(ApplyStrains)
        spec.input('symmetries', valid_type=DataFactory('singlefile'))
        spec.input('symmetry_repr_code', valid_type=Code)

        spec.outline(
            cls.run_apply_strain,
            cls.run_filter_symmetries,
            cls.finalize
        )

    @check_workchain_step
    def run_apply_strain(self):
        self.report('Submitting ApplyStrains workchain.')
        return ToContext(apply_strains=submit(
            ApplyStrains,
            **self.exposed_inputs(ApplyStrains)
        ))

    @check_workchain_step
    def run_filter_symmetries(self):
        self.report('Running FilterSymmetriesCalculation.')
        apply_strains_output = self.ctx.apply_strains.get_outputs_dict()
        tocontext_kwargs = dict()
        process = FilterSymmetriesCalculation.process()
        for strain_value in self.inputs.strain_strengths:
            structure_key = _get_structure_key(strain_value)
            structure_result = apply_strains_output[structure_key]
            self.out(structure_key, structure_result)
            symmetries_key = _get_symmetries_key(strain_value)

            inputs = process.get_inputs_template()
            inputs.code = self.inputs.symmetry_repr_code
            inputs.structure = structure_result
            inputs.symmetries = self.inputs.symmetries
            inputs._options.resources = {'num_machines': 1, 'tot_num_mpiprocs': 1}
            inputs._options.withmpi = False
            tocontext_kwargs[symmetries_key] = submit(
                process,
                **inputs
            )
        return ToContext(**tocontext_kwargs)

    @check_workchain_step
    def finalize(self):
        self.report('Adding filtered symmetries to outputs.')
        for strain_value in self.inputs.strain_strengths:
            symmetries_key = _get_symmetries_key(strain_value)
            self.out(symmetries_key, self.ctx[symmetries_key].out.symmetries)
