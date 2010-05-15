#!/usr/bin/env python
"""ppserver configuration"""

#tunnelports = ['12345','67890']
tunnelports = []

ppservers = tuple(["localhost:%s" % port for port in tunnelports])

# End of file
