import pytest

@pytest.mark.parametrize('strain_kind', [
    'three_five.Biaxial001',
    'three_five.Biaxial110',
    'three_five.Biaxial111',
    'three_five.Uniaxial110',
])
@pytest.mark.parametrize('strain_parameters', [
    'InAs',
    'InSb',
    'GaSb'
])
def test_strains(configure_with_daemon, sample, strain_kind, strain_parameters):
    import pymatgen
    from aiida.orm import DataFactory
    from aiida.orm.data.base import List, Str
    from aiida.work.run import run

    from aiida_strain.work import ApplyStrains

    StructureData = DataFactory('structure')
    structure = StructureData()
    structure.set_pymatgen(pymatgen.Structure.from_file(sample('POSCAR')))

    strain_strengths = List()
    strain_list = [-0.2, -0.1, 0., 0.1, 0.2]
    strain_strengths._set_list(strain_list)

    result = run(
        ApplyStrains,
        structure=structure,
        strain_kind=Str(strain_kind),
        strain_parameters=Str(strain_parameters),
        strain_strengths=strain_strengths
    )

    for s in strain_list:
        key = 'strain_{}'.format(s)
        assert key in result
        assert isinstance(result[key], StructureData)
