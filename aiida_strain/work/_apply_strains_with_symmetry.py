from aiida.orm import DataFactory
from aiida.orm.code import Code
from aiida.work import submit
from aiida.work.workchain import WorkChain, ToContext

from aiida_symmetry_representation.calculations.filter_symmetries import FilterSymmetriesCalculation
from . import ApplyStrains

class ApplyStrainsWithSymmetry(WorkChain):
    @classmethod
    def define(cls, spec):
        super(ApplyStrainsWithSymmetry, cls).define(spec)

        spec.inherit_inputs(ApplyStrains)
        spec.input('symmetries', valid_type=DataFactory('singlefile'))
        spec.input('symmetry_repr_code', valid_type=Code)

        spec.outline(
            cls.run_apply_strain,
            cls.run_filter_symmetries,
            cls.finalize
        )

    def run_apply_strain(self):
        return ToContext(apply_strains=submit(
            ApplyStrains,
            **self.inherited_inputs(ApplyStrains)
        ))

    def run_filter_symmetries(self):
        apply_strains_output = self.ctx.apply_strains.get_outputs_dict()
        strained_structures = {
            key: value for key, value in apply_strains_output.items()
            if key.startswith('structure_') and len(key.split('_')) == 2
        }
        tocontext_kwargs = dict()
        process = FilterSymmetriesCalculation.process()
        for key, structure in strained_structures.items():
            self.out(key, structure)
            suffix = key.split('_', 1)[1]
            inputs = process.get_inputs_template()
            inputs.code = self.inputs.symmetry_repr_code
            inputs.structure = structure
            inputs.symmetries = self.inputs.symmetries
            inputs._options.resources = {'num_machines': 1, 'tot_num_mpiprocs': 1}
            inputs._options.withmpi = False
            tocontext_kwargs['symmetries_{}'.format(suffix)] = submit(
                process,
                **inputs
            )
        return ToContext(**tocontext_kwargs)

    def finalize(self):
        for key, value in self.ctx._get_dict().items():
            if key.startswith('symmetries_'):
                self.out(key, value.out.symmetries)
