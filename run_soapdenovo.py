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
import re
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
parser.add_argument('--kmer', metavar = 'SIZE', type = int, default = 71, help = 'Kmer size to be used for assembly.')
parser.add_argument('--kfile', metavar = 'FILE', nargs = '?', default = '', help = 'File for specifying sample specific kmer sizes.')
parser.add_argument('--execpath', metavar = 'PATH', nargs = '?', default = '', help = 'Directory containing SOAPdenovo2 executables, if they are not in path.')
parser.add_argument('--resultdir', metavar = 'PATH', nargs = '?', default = '', help = 'Directory containing result files.')
parser.add_argument('--slurm', action = 'store_true', help = 'Option for specifying if slurm should be used for job submission.')
args = parser.parse_args()

kmerSizeMap = {}
if args.kfile:
    with open(args.kfile, 'rb') as f:
        for line in f:
            match = re.match('(?P<sample>\d+): (?P<kmer>\d+)', line)
            if match is not None:
                kmerSizeMap[int(match.group('sample'))] = int(match.group('kmer'))

resultDir = args.resultdir
if resultDir:
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)
else:
    resultDir = os.path.abspath(os.path.curdir)

for sample in xrange(1, 25):
    tempName = None
    with tempfile.NamedTemporaryFile(suffix = '.config', delete = False) as temp:
        temp.write(configString.format(directory = os.path.abspath(os.path.curdir), sample = sample))
        tempName = temp.name
    kmerSize = kmerSizeMap.get(sample, args.kmer)
    soapExecutable = 'SOAPdenovo-127mer' if kmerSize > 63 else 'SOAPdenovo-63mer'
    if args.execpath:
      soapExecutable = os.path.join(args.execpath, soapExecutable)
    soapOptions = [soapExecutable, 'all', '-K', str(kmerSize), '-o', '%s/OB00%02d'%(resultDir, sample), '-s', temp.name]
    srunOptions = ['srun', '--output', '%s/OB00%02d.out'%(resultDir, sample), '--error', '%s/OB00%02d.err'%(resultDir, sample)] if args.slurm else []
    print 'Running SOAPdenovo2 for OB00%02d with kmer=%d'%(sample, kmerSize)
    subprocess.call(srunOptions + soapOptions)
