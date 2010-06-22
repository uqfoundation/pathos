# dictionary of known host/profile pairs
profiles = { \
 'upgrayedd.danse.us':'.profile',
 'login.cacr.caltech.edu':'.cshrc',
}
default_profile = '.bash_profile'


def get_profile(rhost):
  '''get the default $PROFILE for a remote host'''
  if profiles.has_key(rhost):
    return profiles[rhost]
  return default_profile

