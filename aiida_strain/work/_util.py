def _get_suffix(strain_value):
    return '_{}'.format(strain_value).replace('.', '_dot_')

def _get_structure_key(strain_value):
    return 'structure' + _get_suffix(strain_value)

def _get_symmetries_key(strain_value):
    return 'symmetries' + _get_suffix(strain_value)
