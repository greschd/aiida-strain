# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines helper functions to convert strain values into the corresponding output keys.
"""


def get_suffix(strain_value: float) -> str:
    return '_{}'.format(strain_value).replace('.', '_dot_').replace('-', '_m_')


def get_structure_key(strain_value: float) -> str:
    return 'structure' + get_suffix(strain_value)


def get_symmetries_key(strain_value: float) -> str:
    return 'symmetries' + get_suffix(strain_value)
