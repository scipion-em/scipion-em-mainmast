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


import os

import pwem

from scipion.install.funcs import VOID_TGZ

from .constants import MAINMAST_HOME, V1_0_0


_logo = "icon.png"
_references = ['MAINMAST']


class Plugin(pwem.Plugin):
    _homeVar = MAINMAST_HOME
    _pathVars = [MAINMAST_HOME]
    _supportedVersions = [V1_0_0]

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(MAINMAST_HOME, 'mainmast-' + cls.getActiveVersion())

    @classmethod
    def isVersion(cls, version='1.0.0'):
        return cls.getActiveVersion().startswith(version)

    @classmethod
    def runSegmentation(cls, protocol, args, cwd=None):
        mainMastCall = os.path.join('%s' % (cls.getHome()), 'mainmast', 'MainmastSeg')
        protocol.runJob(mainMastCall, args, cwd=cwd)

    @classmethod
    def convertMatrix(cls, protocol, args, cwd=None):
        convertCall = os.path.join('%s' % (cls.getHome()), 'mainmast', 'conv_ncs.pl')
        protocol.runJob(convertCall, args, cwd=cwd)

    @classmethod
    def defineBinaries(cls, env):
        mainmast_commands = []
        mainmast_commands.append(('wget -c https://github.com/kiharalab/MAINMASTseg/archive/27828c8.tar.gz', "27828c8.tar.gz"))
        mainmast_commands.append(("tar -xvf 27828c8.tar.gz", []))
        mainmast_commands.append(("mv MAINMASTseg-27828c8* mainmast", []))
        installation_cmd = 'cd mainmast && rm *.o && make -j %s && touch installed' % env.getProcessors()
        mainmast_commands.append((installation_cmd, os.path.join('mainmast', 'installed')))


        env.addPackage('mainmast', version=V1_0_0,
                       commands=mainmast_commands,
                       tar=VOID_TGZ,
                       default=True)
