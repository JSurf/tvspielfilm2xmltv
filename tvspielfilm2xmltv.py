#!/usr/bin/env python
# encoding: utf-8
'''
setup -- shortdesc

setup is a description

It defines classes_and_methods

@author:     user_name
        
@copyright:  2013 organization_name. All rights reserved.
        
@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os, os.path

# Root path
base_path = '/home/chris/tvspielfilm2xmltv' #FIXME: dirty workaround when starting via hardlink
#base_path = os.path.dirname(os.path.abspath(__file__))
print(base_path)
# Insert local directories into path
sys.path.append(os.path.join(base_path))

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from tvsp2xmltv import logger
from tvsp2xmltv import defaults
from tvsp2xmltv import tvsGrabber

__all__ = []
__version__ = 0.2
__date__ = '2013-04-23'
__updated__ = '2013-04-28'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2013 organization_name. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-c", "--controlfile", dest="cfile", action="store", help="create the controlfile [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="option",  help="options from xmltv2vdr call [default: %(default)s]", metavar="option", nargs='*')
        
        # Process arguments
        args = parser.parse_args()
        
        argvline = ""
        for a in sys.argv:
            argvline += a
            argvline += " "
            
        logger.log('Called with following arguments: "'+argvline+'"')
        
        option = args.option
        cfile = args.cfile
        
        if cfile:
            print('Writing Controlfile [' + cfile + ']')
            defaults.write_controlfile(cfile)
            return 0
        
        if option:
            logger.log('Prepare grabbing...')
            grabber = tvsGrabber.TvsGrabber()
            grabber.grab_days = int(option[0])
            
            opt_len = len(option)
            for i in range(3, opt_len):
                #5 ‘‘ 0 ard.de zdf.de
                grabber.add_channel(option[i])
            
            logger.log('Start grabbing...')
            grabber.start_grab()
            logger.log('Saving xml...')
            grabber.save()
            logger.log('End of grabbing...')
            
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        logger.log(program_name + ": " + repr(e) + "\n", logger.ERROR)
        return 2

if __name__ == "__main__":
    if DEBUG:
        #sys.argv.append("-h")
        #sys.argv.append("1 'pin' 0 ard.de zdf.de")
        pass
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'setup_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())