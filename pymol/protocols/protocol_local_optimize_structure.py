# **************************************************************************
# *
# * Authors:     David Herreros Calero (dherreros@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************


from pwem.protocols import ProtAnalysis3D

from pyworkflow.protocol import params
from pwem.objects import AtomStruct
from pyworkflow.utils import Message

from pymol import Plugin


forceFieldList = ['GAFF', 'MMFF94s', 'MMFF94', 'UFF', 'Ghemical']
methodList = ['conjugate gradients', 'steepest descent']


class ProtLocalOptimizeStruct(ProtAnalysis3D):
    """Optimization of atomic structure using Pymol"""
    _label = 'optimize structure'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputPDB', params.PointerParam, label="Input PDB",
                      pointerClass='AtomStruct', important=True,
                      help='Select a PDB to be optimized.')
        form.addParam('method', params.EnumParam,
                      choices=['conjugate gradients', 'steepest descent'], default=0,
                      label='Minimization method',
                      help='The method used to find the local minimum.')
        form.addParam('nSteps', params.IntParam,
                      default=500, label='Minimization steps',
                      help='Number of iteration steps during the minimization.')
        form.addParam('forceField', params.EnumParam,
                      choices=['GAFF', 'MMFF94s', 'MMFF94', 'UFF', 'Ghemical'], default=1,
                      label='Force field',
                      experLevel=params.LEVEL_ADVANCED,
                      help='The forcefield used to compute the Internal Energy.')

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('optimizeStep')
        self._insertFunctionStep('createOutputStep')

    def optimizeStep(self):
        script = self.writeScript()
        Plugin.runPymolScript(self, script)

    def createOutputStep(self):
        pdb = AtomStruct(self._getExtraPath('optimized.pdb'))
        self._defineOutputs(outputPDB=pdb)
        self._defineSourceRelation(self.inputPDB, pdb)

    # --------------------------- UTILS functions ------------------------------
    def writeScript(self):
        script = self._getTmpPath('pymol_optimize.pml')
        forceField = forceFieldList[self.forceField.get()]
        method = methodList[self.method.get()]
        nSteps = self.nSteps.get()
        contents = 'load %s, s1\n' \
                   'import pymol.plugins\n' \
                   'plugins.initialize()\n' \
                   'from pmg_tk.startup.optimize import minimize\n' \
                   'minimize(selection="s1",forcefield="%s",method="%s",nsteps0=%d)\n' \
                   'save %s, s1' % \
                   (self.inputPDB.get().getFileName(), forceField, method,
                    nSteps, self._getExtraPath('optimized.pdb'))
        with open(script, 'w') as fid:
            fid.write(contents)
        return script

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        pass

    def _methods(self):
        pass