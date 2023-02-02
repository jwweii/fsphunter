# fsphunter

This program was developed to locate the genome coordinates by giving the amino acid sequences from the neoantigens derived from frameshift mutations. 
The idea of how program works is: firstly, matching the amino acid sequences to the frameshift transcripts and get the coordinate of those sequences in the transcripts; then, the program takes the advantage of the R package, Ensembldb, to locate the genome coordinates of the amino acid sequence. 

## Docker
To pull down the Docker image, run the following command in your terminal:  
`docker run -it --rm jwweii/fsphunter:"ver6" /bin/bash -c "cd /frameshift_project/ && /bin/bash"`     

For users on WashU Compute1-RIS server:  
`LSF_DOCKER_PRESERVE_ENVIRONMENT=false bsub -G compute-PI_NAME -Is -q general-interactive -a 'docker(jwweii/fsphunter:ver5)' /bin/bash -c "cd ../../frameshift_project/ && /bin/bash"`   
The version of this docker image is different from that for the use in a usual terminal because there seems to be a firewall in Compute1-RIS clusters, where AnnitationHub, a R package, cannot normally work. In this version, the required R object and SQLite file were preloaded in the docker image. 

## fsphunter.py
This is an interactive program, which shows the genome cordinates on the terminal by giving the transcript ID and the frameshift peptide sequence. The command is as below:    

`python3 fsphunter.py tx_id amino_acid_seq` 


### Example for fsphunter.py
For example, by the following command:
`python3 fsphunter.py ENST00000379328 ATLQRSSLW`,

the console will display the following output:  
The length of this tx is 3123   
The peptide is at a forward tx from 2080 to 2107   
The genome coordinate is at chr10 from 8074160 to 8074187   


