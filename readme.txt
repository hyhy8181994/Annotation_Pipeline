##########Data description:############## 

investigated animals: cow, pig, sheep, goat, horse, human, mouse and chicken

Four folders: 
"ORTH" for orthologues informations for each pair of animals obtained from ensembl (March 3th, 2019) and csv files are stored in separate folders named with the corresponding organism name. [ensembl stable gene ID, gene name]

"GO" for gene descriptions for each specie obtained from ensembl (March 3th, 2019). [Gene stable ID, Gene name, Gene start (bp),Gene end (bp), Gene description, Transcript count]
]

"GOD" GO term description of each genes from each specie obtained from ensembl (March 3th, 2019) [Gene stable ID,GO term accession,GO term name,GO term definition]

"OMA" for orthologues information obtained from OMA website (https://omabrowser.org/oma/genomePW/) (March 3th, 2019) [ensmble gene ID specie 1, ensmble gene ID specie 1, type of orthology [1 to many or many to many], OWA group [sets of genes which are all orthologous to one another within group]] 


###########Scripts information#############

Run main.sh file in linux environment or Mac OS (the lastest Ubuntu system is recommended) and following the instructions showed in terminal.

requirements: pandas,numpy,argparse,difflib

Python library can be installed by main script through pip3. If pip3 is not installed, the main script will automatically installed pip. If pip cannot be installed by script, please see https://pip.pypa.io/en/stable/installing/#using-linux-package-managers for possible solutions. 

main script can also download go-basic.obo file from Gene Ontology Consortium website. If the file is already downloaded, you can skip the step.

########Usage of indiviual script########

Usage of data_preparation.py

Description: This script will create a csv file of obsoleted GO term ID and several empty folders (in "New" folder) to save cleaned data. The data cleaning will replace obsoleted GO term ID; Replace empty space of files

python3 data_preparation.py -obo [path of obo file] -path [path of data folder] -outpath [path for output files] -h [help]


Usage of detect_same_or_different_gene.py

Description: This script will output log files for each orthologue files containing orthologue genes with different gene name.

python3 detect_same_or_different_gene.py -path [path of orthologue files] -outpath [path of desired output folder] -h [help]

Usage of Generate_Statistics.py

Description: This script will output log of statistical information of all data

python3 Generate_Statistics.py -path [path of file of data] -outpath [path of desired output folder] -h [help]

Usage of Fuse_Orthologue.py

Description: Fuse Ensembl orthologues file with OMA orthologues file if there is extra information found in OMA files

python3 Fuse_Orthologue.py -path [path of file of data] -outpath [path of desired output folder] -h [help]

Note: it is important to write path as /home/user/Documents/Annotation_pipeline/Data
