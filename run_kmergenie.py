##
# @file run_kmergenie.py
# @brief Script for running kmergenie on all 24 samples.
# @author Ankit Srivastava <asrivast@gatech.edu>
# @version 1.0
# @date 2017-02-20
#
# This script is used for running kmergenie on all 24 samples
# in a directory of FastQ files. It takes a directory containing 'OB00??_fq.gz'
# as input and runs kmergenie on all the paired-end reads. 
#
# Usage:
# python run_kmergenie.py <path to directory>


import glob
import os
import subprocess
import sys
import tempfile

try:
    topDir = sys.argv[1]
except IndexError:
    raise RuntimeError, 'Address of the directory containing FastQ files is required as an argument.'

for num in xrange(1, 25):
    tempName = None
    with tempfile.NamedTemporaryFile(suffix = '.txt', delete = False) as temp:
        fileName = None
        for fileName in glob.glob(os.path.join(topDir, 'OB00%02d_*.fq.gz'%num)):
            temp.write(fileName + '\n')
        if fileName is not None:
            tempName = temp.name
    if tempName is not None:
        subprocess.call(['kmergenie', '-o', 'OB00%02d'%num, tempName])
