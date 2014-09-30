#!/usr/local/bin/python2.7
# encoding: utf-8
'''
pg_change_owner -- 

pg_change_owner is a Change owner on every table view and sequence in a PostgreSql database

It defines classes_and_methods

@author:     Walter Lorenzetti (GIS3W)

@copyright:  2014 GIS3W. All rights reserved.

@license:    GPL3

@contact:    lorenzetti@gis3w.it
@deffield    updated: Updated
'''

import sys
import os
import subprocess
import psycopg2

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2014-09-30'
__updated__ = '2014-09-30'

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

  Created by Walter Lorenzetti (GIS3W) on %s.
  Copyright 2014 GIS3W. All rights reserved.

  Licensed under GPL 3

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-d", "--database", dest="database", help="set the database on to change owner", metavar="DATABASE NAME", required=True)
        parser.add_argument("-e", "--schema", dest="schema", help="set schema to chage owner, defaul il puplic", metavar="DATABASE SCHEMA", default='public' )
        parser.add_argument("-o", "--owner", dest="owner", help="set new owner of database", metavar="NEW OWNER", required=True )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        database = args.database
        schema = args.schema
        owner = args.owner

        #------------------------
        # Change tables owner
        procTables = subprocess.Popen('psql -qAt -c "select tablename from pg_tables where schemaname = \'' + schema + '\';" ' + database,stdout=subprocess.PIPE,shell=True)
        (output, err) = procTables.communicate()
        if err:
            sys.stderr.write(err)
            return 0
        for tb in output.split('\n'):
            if tb != '':
                print tb
                procAlterTables = subprocess.Popen('psql -c "alter table ' + tb + ' owner to ' + owner + '" ' + database,stdout=subprocess.PIPE,shell=True)
                (outputAlterTable, errAlterTable) = procAlterTables.communicate()
                print outputAlterTable
        
        #------------------------
        # Change sequence owner
        procSequences = subprocess.Popen('psql -qAt -c "select sequence_name from information_schema.sequences where sequence_schema = \'' + schema + '\';" ' + database,stdout=subprocess.PIPE,shell=True)
        (outputSequences, errSequence) = procSequences.communicate()
        if errSequence:
            sys.stderr.write(errSequence)
            return 0
        for sq in outputSequences.split('\n'):
            if sq != '':
                print sq
                procAlterSequence = subprocess.Popen('psql -c "alter table ' + sq + ' owner to ' + owner + '" ' + database,stdout=subprocess.PIPE,shell=True)
                (outputAlterSequence, errAlterSequence) = procAlterSequence.communicate()
                print outputAlterSequence
        
        #------------------------
        # Change views owner
        procViews = subprocess.Popen('psql -qAt -c "select table_name from information_schema.views where table_schema = \'' + schema + '\';" ' + database,stdout=subprocess.PIPE,shell=True)
        (outputViews, errView) = procViews.communicate()
        if errView:
            sys.stderr.write(errView)
            return 0
        for vw in outputViews.split('\n'):
            if vw != '':
                print vw
                procAlterView = subprocess.Popen('psql -c "alter table ' + vw + ' owner to ' + owner + '" ' + database,stdout=subprocess.PIPE,shell=True)
                (outputAlterView, errAlterView) = procAlterView.communicate()
                print outputAlterView
            
       
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'pg_change_owner_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())