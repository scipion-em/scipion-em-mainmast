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

MAINMAST_HOME = 'MAINMAST_HOME'

# Supported versions
V1_0_0 = '1.0.0'

PHENIX_TO_SCIPION = {}
PHENIX_CYCLIC = 0  # SYM_CYCLIC = 0
PHENIX_DIHEDRAL_X = 1  # SYM_DIHEDRAL_X = SYM_DIHEDRAL = 1
PHENIX_TETRAHEDRAL = 2  # SYM_TETRAHEDRAL = 3
PHENIX_TETRAHEDRALZ3 = 3  # SYM_TETRAHEDRAL_Z3 = 4
PHENIX_OCTAHEDRAL = 4  # SYM_OCTAHEDRAL = 5
PHENIX_I222 = 5  # SYM_I222 = 6
PHENIX_I222r = 6  # SYM_I222r = 7
PHENIX_In25 = 7  # SYM_In25 = 8
PHENIX_In25r = 8  # SYM_In25r = 9
PHENIX_I2n3 = 9  # SYM_I2n3 = 10
PHENIX_I2n3r = 10  # SYM_I2n3r = 11
PHENIX_I2n5 = 11  # SYM_I2n5 = 12
PHENIX_I2n5r = 12  # SYM_I2n5r = 13

# symmetry dictionary
import pwem.constants as sciSym

PHENIX_TO_SCIPION[PHENIX_CYCLIC] = sciSym.SYM_CYCLIC
PHENIX_TO_SCIPION[PHENIX_DIHEDRAL_X] = sciSym.SYM_DIHEDRAL_X
PHENIX_TO_SCIPION[PHENIX_TETRAHEDRAL] = sciSym.SYM_TETRAHEDRAL
PHENIX_TO_SCIPION[PHENIX_TETRAHEDRALZ3] = sciSym.SYM_TETRAHEDRAL_Z3
PHENIX_TO_SCIPION[PHENIX_OCTAHEDRAL] = sciSym.SYM_OCTAHEDRAL
PHENIX_TO_SCIPION[PHENIX_I222] = sciSym.SYM_I222
PHENIX_TO_SCIPION[PHENIX_I222r] = sciSym.SYM_I222r
PHENIX_TO_SCIPION[PHENIX_In25] = sciSym.SYM_In25
PHENIX_TO_SCIPION[PHENIX_In25r] = sciSym.SYM_In25r
PHENIX_TO_SCIPION[PHENIX_I2n3] = sciSym.SYM_I2n3
PHENIX_TO_SCIPION[PHENIX_I2n3r] = sciSym.SYM_I2n3r
PHENIX_TO_SCIPION[PHENIX_I2n5] = sciSym.SYM_I2n5
PHENIX_TO_SCIPION[PHENIX_I2n5r] = sciSym.SYM_I2n5r

PHENIX_SYM_NAME = dict()
PHENIX_SYM_NAME[PHENIX_CYCLIC] = 'Cn'
PHENIX_SYM_NAME[PHENIX_DIHEDRAL_X] = 'Dn'
PHENIX_SYM_NAME[PHENIX_TETRAHEDRAL] = 'T222'
PHENIX_SYM_NAME[PHENIX_TETRAHEDRALZ3] = 'TZ3'
PHENIX_SYM_NAME[PHENIX_OCTAHEDRAL] = 'O'
PHENIX_SYM_NAME[PHENIX_I222] = 'I222'
PHENIX_SYM_NAME[PHENIX_I222r] = 'I222r'
PHENIX_SYM_NAME[PHENIX_In25] = 'In25'
PHENIX_SYM_NAME[PHENIX_In25r] = 'In25r'
PHENIX_SYM_NAME[PHENIX_I2n3] = 'I2n3'
PHENIX_SYM_NAME[PHENIX_I2n3r] = 'I2n3r'
PHENIX_SYM_NAME[PHENIX_I2n5] = 'I2n5'
PHENIX_SYM_NAME[PHENIX_I2n5r] = 'I2n5r'
