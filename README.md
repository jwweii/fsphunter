# fsphunter

The program is created to locate genome coordinates based on amino acid sequences of neoantigens originating from frameshift mutations. It matches the sequences to the frameshift transcripts to get their transcript coordinates, then uses the Ensembldb R package to find the corresponding genome coordinates. The database used is EnsDb.Hsapiens.v93.

## Docker image
To pull down the Docker image, run the following command in your terminal:  
`docker run -it --rm jwweii/fsphunter:"ver6" /bin/bash -c "cd /frameshift_project/ && /bin/bash"`     

For users on WashU Compute1-RIS server:  
`LSF_DOCKER_PRESERVE_ENVIRONMENT=false bsub -G compute-PI_NAME -Is -q general-interactive -a 'docker(jwweii/fsphunter:ver5)' /bin/bash -c "cd ../../frameshift_project/ && /bin/bash"`   
This version of the docker image differs from the regular terminal version due to the firewall in the Compute1-RIS clusters, which hinders the normal functioning of the R package AnnotationHub. In this version, the necessary R object and SQLite file have been pre-loaded into the docker image.

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

### Suggestion for searching multiple peptide sequences
Although fsphunter.py is convenient for searching transcript coordinates by providing a single neoantigen peptide, it takes about 30 seconds to obtain the genome coordinate from a transcript coordinate due to the requirement of passing the transcript coordinate to the R program, "get_genome_coordinate.R," which imports large R packages such as Ensembldb and AnnotationHub. To more efficiently obtain genome coordinates from multiple neoantigen peptides, it is recommended to import "peptides_locator.py" as a package and use its methods to batch process transcript coordinates before passing them to the R program. This will reduce the need to repeatedly import the R packages.

## peptides_locator.py
As previously stated, "peptides_locator.py" is a python package that provides the functions required by "fsphunter.py." However, it can also be utilized for customized needs, such as batch searching transcript coordinates from multiple peptide sequences.  

### txdict('filename')   
This method loads a transcript dictionary, where the ENST ID is the key and its sequence is the value. The data is obtained from Homo_sapiens.GRCh38.cdna.all.fa. To save time, the dictionary is preloaded as tx_dic.pkl and does not need to be created every time.    
#### example
`import peptides_locator as pl`   
`tx_dict = pl.txdict('tx_dic.pkl').tx_dict`   

### rotationTx(tx=' ')
This method rotates the transcript a base forward and backward. The output is a list with three elements: the output[0] is the normal sequence, the output[1] is the backward rotation of that sequence, and the output[2] is the forward rotation of that sequence. The output could be obtained by the function `get.rotationTx()`.  

#### example
`rotation_tx = pl.rotationTx(tx='ENST00000379328').get_rotationTx()`

### translation(txs=[ ])
This method translates transcript sequences into amino acid sequences. The input is a list of transcript sequences in the order of 'normal', 'backward', and 'forward'. The output is a dictionary with keys 'normal', 'backward', and 'forward' and their corresponding amino acid sequences as values. The output could be obtained by the function `get.rotationAA()`.  

#### example
`rotation_aas = pl.translation(txs=rotation_tx).get_rotationAA()`

### peptide_to_tx(translations= { }, peptide= ' ')
The function inputs a string that represents the peptide sequence and a dictionary that represents the transcript translations into amino acid sequences. It outputs a dictionary with keys "normal", "backward", and "forward", and values as tuples that indicate the start and end coordinates of the peptide sequence within the corresponding transcript. The output could be obtained by the function `get.positions()`.  

#### example
`pep_positions = pl.peptide_to_tx(translations=rotation_aas, peptide='ATLQRSSLW').get_positions()`   

### tx_to_genome(list_to_r=[ ])
This function inputs a list into the R program, get_genome_coordinate.R, using the 'ensembldb' package from R to determine the genome coordinate. The input list should be in the format ['tx_id', start_position_of_the_peptide_in_the_tx, base_width_of_the_target_sequence]. The output will be a list with the first number representing the chromosome number and the second number representing the starting position of the sequence. The output could be obtained by the function `get_gn_coordinate()`.     

#### example
`list_to_r = ['ENST00000379328', 2080, 27]`    
`output = pl.tx_to_genome(list_to_r=list_to_r).get_gn_coordinate()`

### Batch Retrieval of Transcript Coordinates for Multiple Peptides
By using pandas, the transcript coordinates can be obtained as following codes:  
` for index, row in df.iterrows():`  
  `   enst_id = row['tx']`  
  `   peptide = row['peptide']`  
  `   x = tx_dict[enst_id]`  
  `   rotation_tx = pl.rotationTx(tx=x).get_rotationTx()`  
  `   rotation_aas = pl.translation(txs=rotation_tx).get_rotationAA()`  
  `   peptide_positions = pl.peptide_to_tx(translations=rotation_aas, peptide=peptide).get_positions()`   
  `   df.at[index, 'tx_coordinate'] = str(list(peptide_positions.values()))`  
