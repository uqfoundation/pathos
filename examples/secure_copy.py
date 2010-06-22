#!/usr/bin/env python
#

from pathos import SCP_Launcher, SSH_Launcher


if __name__=='__main__':
    source0 = 'test.txt'
    source1 = '~/test.txt'
    source2 = '~/result.txt'
    dest0 = source1
    dest1 = source2
    dest2 = '.'
    cpu1 = 'login.cacr.caltech.edu'
    cpu2 = 'upgrayedd.danse.us'
    del1 = 'rm '+source1
    del2 = 'rm '+source2

   #import journal
    copier = SCP_Launcher('LauncherSCP')
   #journal.debug('LauncherSCP').activate()
    print 'creating %s' % source0
    f = open(source0,'w')
    f.write('Test Successful!\n')
    f.close()

    from time import sleep
    sleep(1) #FIXME: needs time to work...
    print 'executing {scp %s %s:%s}' % (source0,cpu1,dest0)
    copier.stage(source=source0, destination=cpu1+':'+dest0)
    copier.launch()

    sleep(1) #FIXME: needs time to work...
    print 'executing {scp %s:%s %s:%s}' % (cpu1,source1,cpu2,dest1)
    copier.stage(source=cpu1+':'+source1, destination=cpu2+':'+dest1)
    copier.launch()

    sleep(1) #FIXME: needs time to work...
    print 'executing {scp %s:%s %s}' % (cpu2,source2,dest2)
    copier.stage(source=cpu2+':'+source2, destination=dest2)
    copier.launch()

    sleep(1) #FIXME: needs time to work...
    print 'cleanup temporary files...'
    import os
    os.remove(source0)

    launcher = SSH_Launcher('cleanup')
    launcher.stage(command=del1, rhost=cpu1, fgbg='bg')
    launcher.launch()
    launcher.stage(command=del2, rhost=cpu2, fgbg='bg')
    launcher.launch()

#   print 'cleanup result file...'
#   os.remove("."+os.sep+os.path.basename(source2))

# End of file 
