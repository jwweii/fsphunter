# fsphunter

This program was developed to locate the genome coordinate of a frameshift mutation peptide. 


To pull down the Docker image, run the following command in your terminal:  
`docker run -it --rm jwweii/fsphunter:"ver5" /bin/bash -c "cd /frameshift_project/ && /bin/bash"`.   
for users on WashU Compute1-RIS server:  
`LSF_DOCKER_PRESERVE_ENVIRONMENT=false bsub -G compute-PI_NAME -Is -q general-interactive -a 'docker(jwweii/fsphunter:ver5)' /bin/bash -c "cd ../../frameshift_project/ && /bin/bash"`
