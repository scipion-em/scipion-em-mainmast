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


from pwem.protocols import EMProtocol

from pyworkflow.protocol import params
from pwem.objects import AtomStruct
from pyworkflow.utils import Message

from mainmast import Plugin


class ProtMainMastSegmentMap(EMProtocol):
    """Protcol to perform the segmentation of maps into different regions by using
    mainmast software.
    For more information, follow the next link:
    http://kiharalab.org/mainmast_seg/index.html"""
    _label = 'segment map'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        pass

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('segmentStep')
        self._insertFunctionStep('createOutputStep')

    def segmentStep(self):
        pass

    def createOutputStep(self):
        pass

    # --------------------------- UTILS functions ------------------------------


    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        pass

    def _methods(self):
        pass
