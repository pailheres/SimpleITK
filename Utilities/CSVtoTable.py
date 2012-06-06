#!/usr/bin/env python
#=========================================================================
#
#  Copyright Insight Software Consortium
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#=========================================================================

import sys, csv, getopt, re
import os, os.path

"""Create a HTML table from a CSV file that has been generated by CompareITKandSITKFilters.py

By default it reads in filters.csv (the default file produced by CompareITKandSITKFilters.py)
and writes out filters.html.
"""

class bcolors:
    """A class to print colored text."""
    HEADER='\033[95m';  OKBLUE='\033[94m'; OKGREEN='\033[92m';
    WARNING='\033[93m'; FAIL='\033[91m';   ENDC='\033[0m';

def usage():
    """How to use this script"""
    print ""
    print "CSVtoTable.py [options] [input_file [output_file]]"
    print ""
    print "    -h    This help message"
    print "    -d    Make a Doxygen file"
    print ""

#   Variables
#
inname   = "filters.csv"
outname   = "filters.html"
doxyFlag = False

fieldnames      = ( 'Filter', 'ITK', 'SITK', 'Remark', 'ToDo' )    # fields in the CSV file


#
#   Handle command line options
#

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd",
        [ "help", "doxygen" ] )
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-d", "--doxygen"):
        doxyFlag = True
    else:
        assert False, "unhandled option"

#  get the input and output file names
if len(args):
    inname = args[0]
    if len(args)>1:
        outname = args[1]


print inname, outname

if not os.path.isdir( os.path.dirname( outname ) ):
    os.makedirs( os.path.dirname( outname ) )

outfile = open(outname, "w")
color = "FFFFFF"

try:
    if doxyFlag:
        outfile.write( "/** \page Filter_Coverage Filter Coverage\n" )
        outfile.write( "\n" )

    outfile.write( "<table>\n" )
    outfile.write( "<tr>\n" )
    outfile.write( "<th>Filter name</th>\n" )
    outfile.write( "<th>ITK</th>\n" )
    outfile.write( "<th>SimpleITK</th>\n" )
    outfile.write( "<th>Remarks</th>\n" )
    outfile.write( "<th>ToDo</th>\n" )
    outfile.write( "</tr>\n" )

    with open(inname,"rU") as fp:
        reader = csv.DictReader(fp)
        for row in reader:

            filt = row[fieldnames[0]]
            remark = ""
            todo = False

            iflag = sflag = False
            if len(row[fieldnames[1]]):
                iflag = row[fieldnames[1]].lower() == "true"
            if len(row[fieldnames[2]]):
                sflag = row[fieldnames[2]].lower() == "true"

            # Get the remark field from the file.
            if row[fieldnames[3]] != None:
                if len(row[fieldnames[3]]):
                    remark = row[fieldnames[3]]

            # Get the ToDo flag
            if len(row[fieldnames[4]]):
                todo =  row[fieldnames[4]].lower() == "true"

            if sflag:
                if iflag:
                    color = "20FF20"    # Green
                else:
                    color = "C0FFC0"    # Light Green
            else:
                if todo:
                    color = "FFFFFF"    # White
                else:
                    color = "FF7070"    # Red


            outfile.write( "<tr bgcolor="+color+">\n" )
            outfile.write( "<td>"+filt+"</td>\n" )
            outfile.write( "<td>"+str(iflag)+"</td>\n" )
            outfile.write( "<td>"+str(sflag)+"</td>\n" )
            outfile.write( "<td>"+remark+"</td>\n" )
            if not sflag:
                outfile.write( "<td>"+str(todo)+"</td>\n" )
            else:
                outfile.write( "<td></td>\n" )
            outfile.write( "</tr>\n" )

except:
    print "Failed to read input file ", inname
    print sys.exc_info()[0]
    sys.exit(1)

outfile.write( "</table>\n" )

if doxyFlag:
    outfile.write( "*/\n" )

outfile.close()
