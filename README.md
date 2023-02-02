# fsphunter

This program was developed to locate the genome coordinates by giving the amino acid sequences from the neoantigens derived from frameshift mutations. 
The idea of how program works is: firstly, matching the amino acid sequences to the frameshift transcripts and get the coordinate of those sequences in the transcripts; Then, the program takes the advantage of the R package, Ensembldb, to locate the genome coordinates of the amino acid sequence. 


To pull down the Docker image, run the following command in your terminal:  
`docker run -it --rm jwweii/fsphunter:"ver6" /bin/bash -c "cd /frameshift_project/ && /bin/bash"`.     

For users on WashU Compute1-RIS server:  
`LSF_DOCKER_PRESERVE_ENVIRONMENT=false bsub -G compute-PI_NAME -Is -q general-interactive -a 'docker(jwweii/fsphunter:ver5)' /bin/bash -c "cd ../../frameshift_project/ && /bin/bash"`.   
The version of this docker image is different from that for the use in a usual terminal because there seems to be a firewall in Compute1-RIS clusters, where AnnitationHub, a R package, cannot normally work. In this version, the required R object and SQLite file were preloaded in the docker image. 
