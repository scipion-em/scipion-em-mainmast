=============================
Mainmast plugin for Scipion
=============================

MAINMAST is a de novo modeling protocol to build an entire protein 3D model directly from
near-atomic resolution EM map.

=====
Setup
=====

- **Install this plugin in devel mode:**

Using the command line:

.. code-block::

    scipion3 installp -p local/path/to/scipion-em-mainmast --devel

Plugin integration
------------------

The following steps presuppose that you have Anaconda or Miniconda installed on your computer.
In ``~/.config/scipion/scipion.conf`` (Option View > Show Hidden Files must be enabled) or
``path/to/scipion/config/scipion.conf``, set **CONDA_ACTIVATION_CMD** variable in the Packages section.

For example:

.. code-block::

    CONDA_ACTIVATION_CMD = . ~/anaconda3/etc/profile.d/conda.sh
