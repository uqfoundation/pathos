#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component


class Launcher(Component):


    class Inventory(Component.Inventory):

        import pyre.inventory

        nodes = pyre.inventory.int("nodes", default=0)
        nodelist = pyre.inventory.slice("nodelist")


    def launch(self):
        raise NotImplementedError("class '%s' must override 'launch'" % self.__class__.__name__)


    def __init__(self, name, facility="launcher"):
       #Component.__init__(self, name, facility="launcher")
        super(Launcher, self).__init__(name, facility)
        self.nodes = 0
        self.nodelist = None
        return


    def _configure(self):
        self.nodes = self.inventory.nodes
        self.nodelist = self.inventory.nodelist
        return


# version
# file copied from pythia-0.8 pyre.mpi.Launcher.py (svn:danse.us/pyre -r2)

# End of file 
