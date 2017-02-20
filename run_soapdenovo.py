##
# @file run_soapdenovo.py
# @brief Script for running SOAPdenovo2 on paired-end reads. 
# @author Ankit Srivastava <asrivast@gatech.edu>
# @version 1.0
# @date 2017-02-20
#
# Execute the following:
# python run_soapdenovo.py --help
# for usage information.

import argparse
import os
import subprocess
import sys
import tempfile

configString = """
#maximal read length
max_rd_len=250
[LIB]
#average insert size
avg_ins=200
#if sequence needs to be reversed
#in which part(s) the reads are used
#use only first 100 bps of each read
rd_len_cutoff=250
#in which order the reads are used while scaffolding
# cutoff of pair number for a reliable connection (at least 3 for short insert size)
#minimum aligned length to contigs for a reliable read location (at least 32 for short insert size)
#a pair of fastq file, read 1 file should always be followed by read 2 file
q1={directory}/OB00{sample:02d}_R1_val_1.fq.gz
q2={directory}/OB00{sample:02d}_R2_val_2.fq.gz
"""
parser = argparse.ArgumentParser(description='Run SOAPdenovo2 on paired-end reads.')
parser.add_argument('--execpath', metavar = 'PATH', nargs = '?', default = '', help = 'Directory containing SOAPdenovo2 executables, if they are not in path.')
parser.add_argument('--slurm', action = 'store_true', help = 'Option for specifying if slurm should be used for job submission.')
args = parser.parse_args()

for num in xrange(1, 25):
    tempName = None
    with tempfile.NamedTemporaryFile(suffix = '.config', delete = False) as temp:
        temp.write(configString.format(directory = os.path.abspath(os.path.curdir), sample = num))
        tempName = temp.name
    kmerSize = 35 if num in (10, 22) else 61 if num == 19 else 71
    soapExecutable = 'SOAPdenovo-127mer' if kmerSize > 63 else 'SOAPdenovo-63mer'
    if args.execpath:
      soapExecutable = os.path.join(args.execpath, soapExecutable)
    soapOptions = [soapExecutable, 'all', '-K', str(kmerSize), '-o', 'assembly_SOAPdenovo2/OB00%02d'%num, '-s', temp.name]
    srunOptions = ['srun', '--output', 'OB00%02d.out'%num, '--error', 'OB00%02d.err'%num] if args.slurm else []
    subprocess.call(srunOptions + soapOptions)
