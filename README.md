# fsphunter

This program was designed to find genome coordinates based on amino acid sequences from neoantigens arising from frameshift mutations. The program operates as follows: first, it matches the amino acid sequences to the frameshift transcripts and obtains the coordinates of those sequences in the transcripts. Then, it utilizes the Ensembldb R package to find the genome coordinates of the amino acid sequences.

## Docker image
To pull down the Docker image, run the following command in your terminal:  
`docker run -it --rm jwweii/fsphunter:"ver6" /bin/bash -c "cd /frameshift_project/ && /bin/bash"`     

For users on WashU Compute1-RIS server:  
`LSF_DOCKER_PRESERVE_ENVIRONMENT=false bsub -G compute-PI_NAME -Is -q general-interactive -a 'docker(jwweii/fsphunter:ver5)' /bin/bash -c "cd ../../frameshift_project/ && /bin/bash"`   
This version of the docker image differs from the regular terminal version due to the firewall in the Compute1-RIS clusters, which hinders the normal functioning of the R package AnnitationHub. In this version, the necessary R object and SQLite file have been pre-loaded into the docker image.

## fsphunter.py
This is an interactive program that displays genome coordinates in the terminal when provided with a transcript ID and frameshift peptide sequence. The command to run the program is as follows:   

`python3 fsphunter.py tx_id amino_acid_seq`     

### Example for fsphunter.py
For example, by the following command:
`python3 fsphunter.py ENST00000379328 ATLQRSSLW`,

the console will display the following output:  
The length of this tx is 3123   
The peptide is at a forward tx from 2080 to 2107   
The genome coordinate is at chr10 from 8074160 to 8074187  

The fsphunter.py is convenient for searching genome coordinates by providing a single neoantigen peptide. However, it takes about 30 seconds to obtain the genome coordinate from a transcript coordinate due to the requirement of passing the transcript coordinate to the R program, "get_genome_coordinate.R," which imports large R packages such as Ensembldb and AnnotationHub. To more efficiently obtain genome coordinates from multiple neoantigen peptides, it is recommended to import "peptides_locator.py" as a package and use its methods to batch process transcript coordinates before passing them to the R program. This will reduce the need to repeatedly import the R packages.

## peptides_locator.py



