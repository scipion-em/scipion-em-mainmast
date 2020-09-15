# ***************************************************************************
# * Authors:    David Herreros Calero (dherreros@cnb.csic.es)
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
# ***************************************************************************/


import os.path

from pyworkflow.tests import *

from pwem.protocols.protocol_import import (ProtImportPdb,
                                            ProtImportVolumes)
from pwem.constants import (SCIPION_SYM_NAME)

from xmipp3.protocols import (XmippProtConvertPdb)

from ..protocols import ProtMainMastSegmentMap
from phenix.constants import (PHENIX_SYM_NAME, PHENIX_TO_SCIPION, PHENIX_CYCLIC,
                              PHENIX_DIHEDRAL_X, PHENIX_TETRAHEDRAL, PHENIX_OCTAHEDRAL,
                              PHENIX_I)


class TestImportBase(BaseTest):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.dsModBuild = DataSet.getDataSet('model_building_tutorial')

class TestImportData(TestImportBase):
    """ Import map volumes and atomic structures(PDBx/mmCIF files)
    """

    def _importVolume(self, path, samplingRate, label):
        args = {'filesPath': path,
                'samplingRate': samplingRate,
                'setOrigCoord': False
                }
        protImportVol = self.newProtocol(ProtImportVolumes, **args)
        protImportVol.setObjLabel(label)
        self.launchProtocol(protImportVol)
        volume = protImportVol.outputVolume
        return volume

    def _importAtomStruct(self, pdbID, label):
        args = {'inputPdbData': ProtImportPdb.IMPORT_FROM_ID,
                'pdbId': pdbID
                }
        protImportPDB = self.newProtocol(ProtImportPdb, **args)
        protImportPDB.setObjLabel(label)
        self.launchProtocol(protImportPDB)
        structure = protImportPDB.outputPdb
        return structure

    def _convertAtomStruct(self, pdb):
        args = {'inputPdbData': 1,
                'pdbObj': pdb,
                'setSize': True,
                'size': 100
                }
        protConvertPDB = self.newProtocol(XmippProtConvertPdb, **args)
        protConvertPDB.setObjLabel('convert pdb 5ni1')
        self.launchProtocol(protConvertPDB)
        volume = protConvertPDB.outputVolume
        return volume


class TestMainMastSegmentMap(TestImportData):

    pdbID = ["5ni1"]  # Haemoglobin atomic structure

    def testSymO(self):

        # Import Volume
        label = 'import volume apoferritin'
        path = self.dsModBuild.getFile('volumes/emd_9865.map')
        samplingRate = 0.5
        volume = self._importVolume(path, samplingRate, label)

        # import PDB
        # structure = self._importAtomStruct()

        # Convert PDB
        # volume_from_pdb = self._convertAtomStruct(structure)

        # ProtMainMastSegmentMap - Map arguments
        args = {'inputVolume': volume,
                'symmetryGroup': PHENIX_OCTAHEDRAL,
                'threshold': 0.02
                }

        protMainMastSeg1 = self.newProtocol(ProtMainMastSegmentMap,
                                            **args)
        protMainMastSeg1.setObjLabel('MainMast Segmentation - EMD Map')
        self.launchProtocol(protMainMastSeg1)

        seg = protMainMastSeg1.outputMasks
        self.assertTrue(seg.getSize() == 24, "There was a problem with the segmentation")
        self.assertTrue(seg.getSamplingRate() == volume.getSamplingRate(),
                        "Wrong sampling rate in output")
        self.assertTrue(seg.getXDim() == 450,
                        "Wrong dimensions in output")

    def testSymD2(self):

        # Import Volume
        label = 'import volume beta-galactosidase'
        path = self.dsModBuild.getFile('volumes/emd_5995.map')
        samplingRate = 0.64
        volume = self._importVolume(path, samplingRate, label)

        # import PDB
        # structure = self._importAtomStruct()

        # Convert PDB
        # volume_from_pdb = self._convertAtomStruct(structure)

        # ProtMainMastSegmentMap - Map arguments
        args = {'inputVolume': volume,
                'symmetryGroup': PHENIX_DIHEDRAL_X,
                'symmetryOrder': 2,
                'threshold': 0.02
                }

        protMainMastSeg1 = self.newProtocol(ProtMainMastSegmentMap,
                                            **args)
        protMainMastSeg1.setObjLabel('MainMast Segmentation - EMD Map')
        self.launchProtocol(protMainMastSeg1)

        seg = protMainMastSeg1.outputMasks
        self.assertTrue(seg.getSize() == 4, "There was a problem with the segmentation")
        self.assertTrue(seg.getSamplingRate() == volume.getSamplingRate(),
                        "Wrong sampling rate in output")
        self.assertTrue(seg.getXDim() == 340,
                        "Wrong dimensions in output")

    def testSymC2(self):

        # Import Volume
        label = 'import volume haemoglobin'
        path = self.dsModBuild.getFile('volumes/emd_3488.map')
        samplingRate = 1.05
        volume = self._importVolume(path, samplingRate, label)

        # import PDB
        label = 'import pdb 5ni1'
        structure = self._importAtomStruct(self.pdbID[0], label)

        # Convert PDB
        volume_from_pdb = self._convertAtomStruct(structure)

        # ProtMainMastSegmentMap - Map arguments
        args = {'inputVolume': volume,
                'symmetryGroup': PHENIX_CYCLIC,
                'symmetryOrder': 2,
                'threshold': 0.09
                }

        protMainMastSeg1 = self.newProtocol(ProtMainMastSegmentMap,
                                            **args)
        protMainMastSeg1.setObjLabel('MainMast Segmentation - EMD Map')
        self.launchProtocol(protMainMastSeg1)

        seg = protMainMastSeg1.outputMasks
        self.assertTrue(seg.getSize() == 2, "There was a problem with the segmentation")
        self.assertTrue(seg.getSamplingRate() == volume.getSamplingRate(),
                        "Wrong sampling rate in output")
        self.assertTrue(seg.getXDim() == 200,
                        "Wrong dimensions in output")

        # ProtMainMastSegmentMap - Map from PDB arguments
        # FIXME: We need a conversion to CCP4 format (.map) of volume_from_pdb
        # args = {'inputVolume': volume_from_pdb,
        #         'symmetryGroup': PHENIX_CYCLIC,
        #         'symmetryOrder': 2,
        #         'threshold': 0.0
        #         }
        #
        # protMainMastSeg2 = self.newProtocol(ProtMainMastSegmentMap,
        #                                     **args)
        # protMainMastSeg2.setObjLabel('MainMast Segmentation - EMD Map')
        # self.launchProtocol(protMainMastSeg2)

       #  try:
       #      result = eval("protChimera1.DONOTSAVESESSION_Atom_struct__3_%06d.getFileName()"
       #                    % protChimera1.getObjId())
       #  except:
       #      self.assertTrue(False, "There was a problem with the alignment")
       #
       #  self.assertTrue(os.path.exists(result))
       #
       #  # Isolation of asymmetric unit cell of the fitted haemoglobin
       #
       #  extraCommands = ""
       #  extraCommands += "sel #2/A,B\n"
       #  extraCommands += "save /tmp/chainA_B.cif format mmcif models #2 relModel #1 selectedOnly true\n"
       #  extraCommands += "open /tmp/chainA_B.cif\n"
       #  extraCommands += "scipionwrite #3 " \
       #                   "prefix DONOTSAVESESSION_A_B_\n"
       #  extraCommands += "exit\n"
       #
       #  result = eval(
       #      "protChimera1.DONOTSAVESESSION_Atom_struct__3_%06d"
       #      % protChimera1.getObjId())
       #
       #  args = {'extraCommands': extraCommands,
       #          'pdbFileToBeRefined': result
       #          }
       #
       #  protChimera2 = self.newProtocol(ChimeraProtOperate,
       #                                  **args)
       #  protChimera2.setObjLabel('chimera operate\n pdb\n save chain A_B')
       #  self.launchProtocol(protChimera2)
       #
       #  try:
       #      result = eval(
       #          "protChimera2.DONOTSAVESESSION_A_B_Atom_struct__3_%06d.getFileName()"
       #           % protChimera2.getObjId())
       #  except:
       #      self.assertTrue(False,  "There was a problem with the alignment")
       #
       #  self.assertTrue(os.path.exists(result))
       #
       #
       # # Generation of map from the asymmetric unit cell
       #
       #  extraCommands = ""
       #  extraCommands += "sym #3 C2 copies t"  ## method for all symmetries: symMethod defined in
       #                                         ## scipion-em-chimera/chimera/protocols/protocol_subtraction_maps.py (class ChimeraSubtractionMaps)
       #  extraCommands += "delete #4 & #3 #>3"
       #  extraCommands += "molmap #4 3 gridSpacing 1.05"  # 3 resolution
       #  extraCommands += "scipionwrite #5 " \
       #                   "prefix molmap_resolution_3_\n"
       #  extraCommands += "exit\n"
       #
       #  result = eval(
       #          "protChimera2.DONOTSAVESESSION_A_B_Atom_struct__3_%06d"
       #           % protChimera2.getObjId())
       #
       #  args = {'extraCommands': extraCommands,
       #          'pdbFileToBeRefined': result
       #          }
       #
       #  protChimera3 = self.newProtocol(ChimeraProtOperate,
       #                                  **args)
       #  protChimera3.setObjLabel('chimera operate\n map from model\n')
       #  self.launchProtocol(protChimera3)
       #
       #  try:
       #      result = eval(
       #          "protChimera3.molmap_resolution_3__Map_5_%06d.getFileName()"
       #           % protChimera3.getObjId())
       #  except:
       #      self.assertTrue(False,  "There was a problem with the alignment")
       #
       #  self.assertTrue(os.path.exists(result))
