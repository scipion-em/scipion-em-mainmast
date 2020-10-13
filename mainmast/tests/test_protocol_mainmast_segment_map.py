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

from pwem.protocols.protocol_import import (ProtImportPdb, ProtImportVolumes)

from xmipp3.protocols import (XmippProtConvertPdb)

from ..protocols import ProtMainMastSegmentMap
from phenix.constants import (PHENIX_CYCLIC, PHENIX_DIHEDRAL_X,
                              PHENIX_TETRAHEDRAL, PHENIX_OCTAHEDRAL,
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

    def _convertAtomStruct(self, pdb, size, samplingRate, label):
        args = {'inputPdbData': 1,
                'pdbObj': pdb,
                'setSize': True,
                'size': size,
                'sampling': samplingRate
                }
        protConvertPDB = self.newProtocol(XmippProtConvertPdb, **args)
        protConvertPDB.setObjLabel(label)
        self.launchProtocol(protConvertPDB)
        volume = protConvertPDB.outputVolume
        return volume


class TestMainMastSegmentMap(TestImportData):

    pdbID = ["5ni1", "6vyg", "6sht", "", "4ci0", "6n1r"]  # Haemoglobin atomic structure

    def testSymT(self):

        # Import Volume
        label = 'import volume GyrA N-terminal fragment'
        path = self.dsModBuild.getFile('volumes/emd_9318.map')
        samplingRate = 0.87
        volume = self._importVolume(path, samplingRate, label)

        # # import PDB
        # label = "import pdb 6n1r"
        # structure = self._importAtomStruct(self.pdbID[4], label)
        #
        # # Convert PDB
        # label = 'convert pdb 6n1r'
        # size = 224
        # volume_from_pdb = self._convertAtomStruct(structure, size,
        #                                           samplingRate, label)

        # ProtMainMastSegmentMap - Map arguments
        args = {'inputVolume': volume,
                'symmetryGroup': PHENIX_TETRAHEDRAL,
                'threshold': 0.0374
                }

        protMainMastSeg1 = self.newProtocol(ProtMainMastSegmentMap, **args)
        protMainMastSeg1.setObjLabel('MainMast Segmentation - EMD Map')
        self.launchProtocol(protMainMastSeg1)

        seg = protMainMastSeg1.outputMasks
        self.assertTrue(seg.getSize() == 12,
                        "There was a problem with the segmentation")
        self.assertTrue(seg.getSamplingRate() == volume.getSamplingRate(),
                        "Wrong sampling rate in output")
        self.assertTrue(seg.getXDim() == 548,
                        "Wrong dimensions in output")

    # FIXME: I Symmetry is apparently not working (in the article is barely mentioned)
    # def testSymI(self):
    #
    #     # Import Volume
    #     label = 'import volume MS2 Virus-like-particle'
    #     path = self.dsModBuild.getFile('volumes/emd_4990.map')
    #     samplingRate = 1.03
    #     volume = self._importVolume(path, samplingRate, label)
    #
    #     # # import PDB
    #     # label = "import pdb 6dzu"
    #     # structure = self._importAtomStruct(self.pdbID[3], label)
    #     #
    #     # # Convert PDB
    #     # label = 'convert pdb 6dzu'
    #     # size = 256
    #     # volume_from_pdb = self._convertAtomStruct(structure, size,
    #     #                                           samplingRate, label)
    #
    #     # ProtMainMastSegmentMap - Map arguments
    #     args = {'inputVolume': volume,
    #             'symmetryGroup': PHENIX_I,
    #             'threshold': 0.04
    #             }
    #
    #     protMainMastSeg1 = self.newProtocol(ProtMainMastSegmentMap, **args)
    #     protMainMastSeg1.setObjLabel('MainMast Segmentation - EMD Map')
    #     self.launchProtocol(protMainMastSeg1)
    #
    #     seg = protMainMastSeg1.outputMasks
    #     self.assertTrue(seg.getSize() == 24,
    #                     "There was a problem with the segmentation")
    #     self.assertTrue(seg.getSamplingRate() == volume.getSamplingRate(),
    #                     "Wrong sampling rate in output")
    #     self.assertTrue(seg.getXDim() == 400,
    #                     "Wrong dimensions in output")

    # def testSymO(self):
    #
    #     # Import Volume
    #     label = 'import volume apoferritin'
    #     path = self.dsModBuild.getFile('volumes/emd_10205.map')
    #     samplingRate = 0.96
    #     volume = self._importVolume(path, samplingRate, label)
    #
    #     # # import PDB
    #     # label = "import pdb 6sht"
    #     # structure = self._importAtomStruct(self.pdbID[2], label)
    #     #
    #     # # Convert PDB
    #     # label = 'convert pdb 6sht'
    #     # size = 256
    #     # volume_from_pdb = self._convertAtomStruct(structure, size,
    #     #                                           samplingRate, label)
    #
    #     # ProtMainMastSegmentMap - Map arguments
    #     args = {'inputVolume': volume,
    #             'symmetryGroup': PHENIX_OCTAHEDRAL,
    #             'threshold': 0.05
    #             }
    #
    #     protMainMastSeg1 = self.newProtocol(ProtMainMastSegmentMap, **args)
    #     protMainMastSeg1.setObjLabel('MainMast Segmentation - EMD Map')
    #     self.launchProtocol(protMainMastSeg1)
    #
    #     seg = protMainMastSeg1.outputMasks
    #     self.assertTrue(seg.getSize() == 24,
    #                     "There was a problem with the segmentation")
    #     self.assertTrue(seg.getSamplingRate() == volume.getSamplingRate(),
    #                     "Wrong sampling rate in output")
    #     self.assertTrue(seg.getXDim() == 256,
    #                     "Wrong dimensions in output")
    #
    # def testSymD2(self):
    #
    #     # Import Volume
    #     label = 'import volume plasmodium'
    #     path = self.dsModBuild.getFile('volumes/emd_21459.map')
    #     samplingRate = 0.84
    #     volume = self._importVolume(path, samplingRate, label)
    #
    #     # # import PDB
    #     # label = "import pdb 6vyg"
    #     # structure = self._importAtomStruct(self.pdbID[1], label)
    #     #
    #     # # Convert PDB
    #     # label = 'convert pdb 6vyg'
    #     # size = 256
    #     # volume_from_pdb = self._convertAtomStruct(structure, size,
    #     #                                           samplingRate, label)
    #
    #     # ProtMainMastSegmentMap - Map arguments
    #     args = {'inputVolume': volume,
    #             'symmetryGroup': PHENIX_DIHEDRAL_X,
    #             'symmetryOrder': 2,
    #             'threshold': 0.01
    #             }
    #
    #     protMainMastSeg1 = self.newProtocol(ProtMainMastSegmentMap, **args)
    #     protMainMastSeg1.setObjLabel('MainMast Segmentation - EMD Map')
    #     self.launchProtocol(protMainMastSeg1)
    #
    #     seg = protMainMastSeg1.outputMasks
    #     self.assertTrue(seg.getSize() == 4,
    #                     "There was a problem with the segmentation")
    #     self.assertTrue(seg.getSamplingRate() == volume.getSamplingRate(),
    #                     "Wrong sampling rate in output")
    #     self.assertTrue(seg.getXDim() == 256,
    #                     "Wrong dimensions in output")
    #
    # def testSymC2(self):
    #
    #     # Import Volume
    #     label = 'import volume haemoglobin'
    #     path = self.dsModBuild.getFile('volumes/emd_3488.map')
    #     samplingRate = 1.05
    #     volume = self._importVolume(path, samplingRate, label)
    #
    #     # # import PDB
    #     # label = 'import pdb 5ni1'
    #     # structure = self._importAtomStruct(self.pdbID[0], label)
    #     #
    #     # # Convert PDB
    #     # label = 'convert pdb 5ni1'
    #     # size = 100
    #     # volume_from_pdb = self._convertAtomStruct(structure, size,
    #     #                                           samplingRate, label)
    #
    #     # ProtMainMastSegmentMap - Map arguments
    #     args = {'inputVolume': volume,
    #             'symmetryGroup': PHENIX_CYCLIC,
    #             'symmetryOrder': 2,
    #             'threshold': 0.09
    #             }
    #
    #     protMainMastSeg1 = self.newProtocol(ProtMainMastSegmentMap, **args)
    #     protMainMastSeg1.setObjLabel('MainMast Segmentation - EMD Map')
    #     self.launchProtocol(protMainMastSeg1)
    #
    #     seg = protMainMastSeg1.outputMasks
    #     self.assertTrue(seg.getSize() == 2,
    #                     "There was a problem with the segmentation")
    #     self.assertTrue(seg.getSamplingRate() == volume.getSamplingRate(),
    #                     "Wrong sampling rate in output")
    #     self.assertTrue(seg.getXDim() == 200,
    #                     "Wrong dimensions in output")

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
