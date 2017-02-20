#!/usr/bin/env perl

# Shashwat Deepali Nagar, 2017
# Jordan Lab, Georgia Tech

# Script for running SPAdes for all the reads in a directory.

my $outDir = "/data/home/snagar9/data/compGenomics/assemblies/spades/all_clip18";
my $inDir = "/data/home/snagar9/data/compGenomics/trimmedReads_otherServer/option1";

my ($read1, $read2);
chomp(my @fileList = `ls $inDir | awk '{if(\$0 !~ /README/ && \$0 !~ /trim_galore/){print;}}'`);

for (my $i = 0; $i < scalar @fileList; $i++) {
  $read1 = $fileList[$i];
  $read1 =~ /(OB\d\d\d\d)/;
  $i += 1;
  $read2 = $fileList[$i];
  `mkdir $outDir/$1`;
  `spades.py -1 $inDir/$read1 -2 $inDir/$read2 --careful --mismatch-correction -o $outDir/$1`;
}
