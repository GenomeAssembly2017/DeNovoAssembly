# DeNovoAssembly

This repository is meant to collaborate on _de novo_ assembly related material. Following is a list of the files/data in this repository: (Please modify this file if you decide to change something.)

* `run_kmergenie.py` is a Python script for running kmergenie (surprise!) on paired-end reads and determining most suitable kmer size for each of the samples.

*  `bulkSpades.pl` is a Perl script for running SPAdes on paired end reads. Just specify the in/out directories and modify SPAdes parameters in the script.

* `run_soapdenovo.py` is a Python script for running SOAPdenovo2 on paired-end read samples. Refer to the file for more information on the options, etc.
