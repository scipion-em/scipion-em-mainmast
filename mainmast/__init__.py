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
from .constants import MAINMAST_HOME, V1_0_0

_logo = "icon.gih"
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
    def runMainMastScript(cls, protocol, args):
        mainMastCall = os.path.join('%s' % (cls.getHome()), 'MainmastSeg')
        protocol.runJob(mainMastCall, args)

    @classmethod
    def convertMST(cls, protocol, args):
        convertCall = os.path.join('%s' % (cls.getHome()), 'bondtreeCIF.pl')
        protocol.runJob(convertCall, args)

    @classmethod
    def defineBinaries(cls, env):
        SW_EM = env.getEmFolder()

        installationCmd = 'rm *.o && make -j %s && ' % env.getProcessors()
        installationCmd += 'cd .. && mv MAINMASTseg-27828c8746d0d85d99708a66af1f81cb173ed626 mainmast'

        mainmast_commands = [(installationCmd, os.path.join("%s" % SW_EM, "mainmast"))]

        env.addPackage('mainmast', version=V1_0_0,
                       url='https://github.com/kiharalab/MAINMASTseg/archive/27828c8.tar.gz',
                       buildDir='MAINMASTseg-27828c8746d0d85d99708a66af1f81cb173ed626',
                       commands=mainmast_commands,
                       targetDir='mainmast',
                       default=True)
