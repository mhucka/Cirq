.. |cirqlogo| image:: https://raw.githubusercontent.com/quantumlib/Cirq/refs/heads/main/docs/images/Cirq_logo_color.svg
   :alt: Cirq logo
   :target: https://github.com/quantumlib/cirq
   :height: 80px

.. |rigettilogo| image:: https://upload.wikimedia.org/wikipedia/commons/0/09/Rigetti_Computing_logo.svg
   :alt: Rigetti logo
   :target: https://rigetti.com/
   :height: 55px

.. |cirq| replace:: Cirq
.. _cirq: https://github.com/quantumlib/cirq

.. |cirq-docs| replace:: Cirq documentation site
.. _cirq-docs: https://quantumai.google/cirq

.. |cirq-github| replace:: Cirq GitHub repository
.. _cirq-github: https://github.com/quantumlib/Cirq

.. |cirq-rigetti| replace:: ``cirq-rigetti``
.. |cirq-core| replace:: ``cirq-core``

.. class:: centered
.. Note: the space between the following items uses no-break spaces.

|cirqlogo|                |rigettilogo|

This Python module is |cirq-rigetti|, which provides everything you'll need to run
|cirq|_ quantum algorithms on quantum computers made by `Rigetti Computing
<https://rigetti.com/>`__.

|cirq|_ is a Python package for writing, manipulating, and running `quantum
circuits <https://en.wikipedia.org/wiki/Quantum_circuit>`__ on quantum
computers and simulators. Cirq provides useful abstractions for dealing with
today’s `noisy intermediate-scale quantum <https://arxiv.org/abs/1801.00862>`__
(NISQ) computers, where the details of quantum hardware are vital to achieving
state-of-the-art results. For more information about Cirq, please visit the
|cirq-docs|_.


Installation
------------

This module is built on top of |cirq|_; installing this module will
automatically install |cirq-core| and other dependencies. There are two
installation options for the |cirq-rigetti| module:

* To install the stable version of |cirq-rigetti|, use ``pip install cirq-rigetti``.

* To install the pre-release version of |cirq-rigetti|, use ``pip install
  cirq-rigetti~=1.0.dev``. (The ``~=`` has a special meaning to ``pip`` of
  selecting the latest version compatible with the ``1.*`` and ``dev`` in the
  name. Despite appearances, this will not install an old version 1.0 release!)

If you would like to install Cirq with all the optional modules, not just
|cirq-rigetti|, then instead of the above commands, use ``pip install cirq`` for
the stable release or ``pip install cirq~=1.0.dev`` for the latest pre-release
version.


Documentation
-------------

To get started with using Rigetti quantum computers through Cirq, please refer to
the following documentation:

* `Access and authentication <https://quantumai.google/cirq/rigetti/access>`__

* `Getting started guide
  <https://quantumai.google/cirq/tutorials/rigetti/getting_started>`__

To get started with using Cirq in general, please refer to the |cirq-docs|_.

For more information about getting help, reporting bugs, and other matters
related to Cirq and the Cirq-Rigetti integration module, please visit the
|cirq-github|_.


Disclaimer
----------

Cirq is not an official Google product. Copyright 2019 The Cirq Developers
