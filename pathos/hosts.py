# dictionary of known host/profile pairs
"""
_profiles = { \
 'upgrayedd.danse.us':'.profile',
 'login.cacr.caltech.edu':'.cshrc',
}
"""

_profiles = { }
default_profile = '.bash_profile'

def get_profile(rhost, assume=True):
  '''get the default $PROFILE for a remote host'''
  if _profiles.has_key(rhost):
    return _profiles[rhost]
  if assume:
    return default_profile
  return 


def get_profiles():
  '''get $PROFILE for each registered host'''
  return _profiles


def register_profiles(profiles):
  '''add dict of {'host':$PROFILE} to registered host profiles'''
  #XXX: needs parse checking of input
  _profiles.update(profiles)
  return


def register(rhost, profile=None):
  '''register a host and $PROFILE'''
  if profile == None:
    profile = default_profile
  #XXX: needs parse checking of input
  _profiles[rhost] = profile
  return 


# EOF
