.. © 2017-2019, ETH Zurich, Institut für Theoretische Physik
.. Author: Dominik Gresch <greschd@gmx.ch>

Tutorial
========

This tutorial will take you through a calculation using ``aiida-strain``. It assumes that you are already familiar with using AiiDA.

Creating strained structures
----------------------------

To create strained structures, you can use the :class:`.ApplyStrains` workflow. It requires an input (unstrained) AiiDA structure, and parameters that indicate which kind of strain should be applied:

* ``strain_kind`` is the name of a :mod:`strain.structure` subclass, that governs how the strain is applied.
* ``strain_parameters`` is the name of a :mod:`strain.parameter` instance, which gives the material-specific strain parameters.
* ``strain_strengths`` is a list of strain values for which the strained structure should be calculated

In the following example, we apply -2\%, -1\%, 1\% and 2\% uni-axial (110) strain to unstrained InSb:

.. include:: ../../examples/InSb/run_strain.py
    :code: python

Filtering symmetries
--------------------

In addition to creating strained structures, you can also find out which symmetries the strained structure respects. To do that, use the :class:`ApplyStrainsWithSymmetry` workflow, and add as an additional input a file describing the symmetries in :mod:`symmetry_representation` HDF5 format:

.. include:: ../../examples/InSb/run_strain_with_symmetries.py
    :code: python

For this example, you also need to have the `symmetry-repr` command line utility available as an AiiDA code.

.. note:: The input files and source for the examples can be found on the `aiida-strain GitHub <https://github.com/greschd/aiida-strain>`_.
