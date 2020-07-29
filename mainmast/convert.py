# **************************************************************************
# *
# * Authors:    David Herreros Calero (dherreros@cnb.csic.es)
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
from pwem.constants import SCIPION_SYM_NAME
from .constants import (PHENIX_SYM_NAME, PHENIX_TO_SCIPION, PHENIX_CYCLIC,
                         PHENIX_DIHEDRAL_X, PHENIX_TETRAHEDRAL,
                         PHENIX_TETRAHEDRALZ3, PHENIX_OCTAHEDRAL,
                         PHENIX_I222, PHENIX_I222r, PHENIX_In25, PHENIX_In25r,
                         PHENIX_I2n5, PHENIX_I2n5r, PHENIX_I2n3, PHENIX_I2n3r,
                         )
PHENIX_LIST = [PHENIX_SYM_NAME[PHENIX_CYCLIC] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_CYCLIC]] + ")",
                               PHENIX_SYM_NAME[PHENIX_DIHEDRAL_X] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_DIHEDRAL_X]] + ")",
                               PHENIX_SYM_NAME[PHENIX_TETRAHEDRAL] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_TETRAHEDRAL]] + ")",
                               PHENIX_SYM_NAME[PHENIX_TETRAHEDRALZ3] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_TETRAHEDRALZ3]] + ")",
                               PHENIX_SYM_NAME[PHENIX_OCTAHEDRAL] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_OCTAHEDRAL]] + ")",
                               PHENIX_SYM_NAME[PHENIX_I222] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_I222]] + ")",
                               PHENIX_SYM_NAME[PHENIX_I222r] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_I222r]] + ")",
                               PHENIX_SYM_NAME[PHENIX_In25] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_In25]] + ")",
                               PHENIX_SYM_NAME[PHENIX_In25r] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_In25r]] + ")",
                               PHENIX_SYM_NAME[PHENIX_I2n3] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_I2n3]] + ")",
                               PHENIX_SYM_NAME[PHENIX_I2n3r] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_I2n3r]] + ")",
                               PHENIX_SYM_NAME[PHENIX_I2n5] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_I2n5]] + ")",
                               PHENIX_SYM_NAME[PHENIX_I2n5r] +
                               " (" + SCIPION_SYM_NAME[PHENIX_TO_SCIPION[PHENIX_I2n5r]] + ")",
                               ]