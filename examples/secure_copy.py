#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
example of using the secure copy interface

To run: python secure_copy.py
"""

from pathos.secure import Copier, Pipe


if __name__=='__main__':
    source0 = 'test.txt'
    source1 = '~/test.txt'
    source2 = '~/result.txt'
    dest0 = source1
    dest1 = source2
    dest2 = '.'
    cpu1 = 'localhost'
    cpu2 = 'localhost'
   #cpu1 = 'computer.cacr.caltech.edu'
   #cpu2 = 'foobar.danse.us'
    del1 = 'rm '+source1
    del2 = 'rm '+source2

    copier = Copier('LauncherSCP')
    print('creating %s' % source0)
    f = open(source0,'w')
    f.write('Test Successful!\n')
    f.close()

    from time import sleep
    sleep(1) #FIXME: needs time to work...
    print('executing {scp %s %s:%s}' % (source0,cpu1,dest0))
    copier(source=source0, destination=cpu1+':'+dest0)
    copier.launch()

    sleep(1) #FIXME: needs time to work...
    print('executing {scp %s:%s %s:%s}' % (cpu1,source1,cpu2,dest1))
    copier(source=cpu1+':'+source1, destination=cpu2+':'+dest1)
    copier.launch()

    sleep(1) #FIXME: needs time to work...
    print('executing {scp %s:%s %s}' % (cpu2,source2,dest2))
    copier(source=cpu2+':'+source2, destination=dest2)
    copier.launch()

    sleep(1) #FIXME: needs time to work...
    print('cleanup temporary files...')
    import os
    os.remove(source0)

    launcher = Pipe('cleanup')
    launcher(command=del1, host=cpu1, background=True)
    launcher.launch()
    launcher(command=del2, host=cpu2, background=True)
    launcher.launch()

#   print('cleanup result file...')
#   os.remove("."+os.sep+os.path.basename(source2))

# End of file 
