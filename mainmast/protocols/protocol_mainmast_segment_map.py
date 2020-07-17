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


import os, glob
import numpy as np

from pwem.protocols import EMProtocol
from pyworkflow.protocol import params
from pwem.emlib.image import ImageHandler
from pwem.objects import Volume

from mainmast import Plugin as Mainmast
from phenix import Plugin as Phenix


class ProtMainMastSegmentMap(EMProtocol):
    """Protcol to perform the segmentation of maps into different regions by using
    mainmast software.
    For more information, follow the next link:
    http://kiharalab.org/mainmast_seg/index.html"""
    _label = 'segment map'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label='Input data')
        form.addParam('inputVolume', params.PointerParam, pointerClass='Volume', label='Input volume', important=True,
                      help='Select a Volume to be segmented.')
        form.addParam('sym', params.StringParam, label='Map symmetry',
                      help='Point group symmetry of input volume (all point group symmetries are allowed '
                           'except C1).')
        form.addParam('threshold', params.FloatParam, default=0.0, label='Threshold',
                      help='Threshold of density map.')
        form.addParam('combine', params.BooleanParam, default=False, label='Combine masks?',
                      help='If yes, all the segmented regions detected will be combine into a '
                           'single identifier mask.')
        form.addParallelSection(threads=4, mpi=0)

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('createSymmetryMatrixStep')
        self._insertFunctionStep('segmentStep')
        self._insertFunctionStep('createOutputStep')

    def createSymmetryMatrixStep(self):
        pathMap = os.path.abspath(self.inputVolume.get().getFileName())
        args = '%s symmetry=%s' % (pathMap, self.sym.get())
        Phenix.runPhenixProgram(Phenix.getProgram('map_symmetry.py'), args, cwd=self._getExtraPath())
        args = '%s > sym_mat.txt' % ('symmetry_from_map.ncs_spec')
        Mainmast.convertMatrix(self, args, cwd=self._getExtraPath())

    def segmentStep(self):
        pathMap = os.path.abspath(self.inputVolume.get().getFileName())
        pathMatrix = os.path.abspath(self._getExtraPath('sym_mat.txt'))
        args = '-i %s -Y %s -c %d -t %f -M -W > contour.cif' % (pathMap, pathMatrix, self.numberOfThreads.get(),
                                                                self.threshold.get())
        Mainmast.runSegmentation(self, args, cwd=self._getExtraPath())

    def createOutputStep(self):
        if self.combine.get():
            ih = ImageHandler()
            outMask = ih.createImage()
            for idx, image in enumerate(sorted(glob.glob(self._getExtraPath("region*.mrc")))):
                region = ih.read(image).getData()
                region *= (idx+1)
                if idx == 0:
                    outData = np.zeros(region.shape, float)
                outData += region
            outMask.setData(outData)
            ih.write(outMask, self._getExtraPath('outMask.mrc'))
            volume = Volume()
            volume.setSamplingRate(self.inputVolume.get().getSamplingRate())
            volume.setLocation(self._getExtraPath('outMask.mrc'))
            self._defineOutputs(outputMask=volume)
            self._defineSourceRelation(self.inputVolume, volume)
        else:
            outSet = self._createSetOfVolumes()
            samplingRate = self.inputVolume.get().getSamplingRate()
            outSet.setSamplingRate(samplingRate)
            for image in sorted(glob.glob(self._getExtraPath("region*.mrc"))):
                volume = Volume()
                volume.setSamplingRate(samplingRate)
                volume.setLocation(image)
                outSet.append(volume)
            self._defineOutputs(outputMasks=outSet)
            self._defineSourceRelation(self.inputVolume, outSet)

    # --------------------------- UTILS functions ------------------------------


    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        summary = []
        summary.append("Input Volume provided: %s\n"
                       % self.inputVolume.get().getFileName())
        if self.getOutputsSize() >= 1:
            regions = len(glob.glob(self._getExtraPath("region*.mrc")))
            if hasattr(self, 'outputMasks'):
                msg = ("A total of %d regions have been segmented" % regions)
                summary.append(msg)
            if hasattr(self, 'outputMask'):
                msg = ("Output regions combined to an indentifier mask with %d different "
                       "regions" % regions)
                summary.append(msg)
        else:
            summary.append("Segmentation not ready yet.")
        return summary

    def _methods(self):
        methodsMsgs = []
        methodsMsgs.append('*Input volume:* %s' % self.inputVolume.get().getFileName())
        methodsMsgs.append('*Map symmetry:* %s' % self.sym.get())
        methodsMsgs.append('*Map threshold:* %d' % self.threshold.get())
        methodsMsgs.append('*Regions combined:* %r' % self.combine.get())
        if self.getOutputsSize() >= 1:
            regions = len(glob.glob(self._getExtraPath("region*.mrc")))
            msg = ("*Regions segmented:* %d" % regions)
            methodsMsgs.append(msg)
        else:
            methodsMsgs.append("Segmentation not ready yet.")
        return methodsMsgs

