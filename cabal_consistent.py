#!/usr/bin/python

import subprocess
import os
import fnmatch
from argparse import ArgumentParser

if __name__ == '__main__':
    # Options
    parser = ArgumentParser(description='cabal consistent upgrade')
    parser.add_argument('-i', '--ignore-cabal', action='store_true',
                        help='Ignore .cabal file if it exists.')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Don\'t ask for confirmation.')
    args = parser.parse_args()
    
    # User packs
    user_packs = sorted(subprocess.check_output(['ghc-pkg', 'list', '--user', 
                  '--simple-output', '--names-only']).split())
    
    # What keeping
    glob_packs = sorted(subprocess.check_output(['ghc-pkg', 'list', '--global', 
                  '--simple-output', '--names-only']).split())
    exclude_from_cons = list(set(glob_packs) & set(user_packs))
    glob_packs = sorted(list(set(glob_packs)
                             .difference(set(exclude_from_cons))))
    what_keep = ["--constraint=" + p + " installed" for p in glob_packs]
    
    # what updating
    what_up = user_packs
    cabal_exists = not len(fnmatch.filter(os.listdir('.'), "*.cabal")) == 0
    if (not args.ignore_cabal) and cabal_exists:
        what_up = ['--only-dependencies', '--upgrade-dependencies']
        print '.cabal found. Upgrading local pependencies.'
     
    if not args.quiet:
        subprocess.call(["cabal", "install", "--dry-run", '--force-reinstalls'] 
                        + what_keep 
                        + what_up)
        raw_input("Press any key to accept or [Ctrl-C] to cancel")
        
    subprocess.call(["cabal", "install", '--force-reinstalls'] + what_keep 
                    + what_up)
