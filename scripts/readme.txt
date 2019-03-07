Data description: 

investigated animals: cow, pig, sheep, goat, horse, human, mouse and chicken

Four folders: 
"ORTH" for orthologues informations for each pair of animals obtained from ensembl (March 3th, 2019) and csv files are stored in separate folders named with the corresponding organism name. [ensembl stable gene ID, gene name]

"GO" for gene descriptions for each specie obtained from ensembl (March 3th, 2019). [Gene stable ID, Gene name, Gene start (bp),Gene end (bp), Gene description, Transcript count]
]

"GOD" GO term description of each genes from each specie obtained from ensembl (March 3th, 2019) [Gene stable ID,GO term accession,GO term name,GO term definition]

"OMA" for orthologues information obtained from OMA website (https://omabrowser.org/oma/genomePW/) (March 3th, 2019) [ensmble gene ID specie 1, ensmble gene ID specie 1, type of orthology [1 to many or many to many], OWA group [sets of genes which are all orthologous to one another within group]] 


Scripts information

requirements: pandas,numpy,argparse,difflib

Usage of Data_pre_proccess

Description: This script will create a csv file of obsoleted GO term ID and several empty folders (in "New" folder) to save cleaned data. The data cleaning will replace obsoleted GO term ID; Replace empty space of files

python3 Data_pre.py -obo [path of obo file] -path [path of data folder] -outpath [path for output files] -h [help]


Usage of same_gene

Description: This script will output log files for each orthologue files containing orthologue genes with different gene name.

python3 same_gene.py -path [path of orthologue files] -outpath[path of desired output folders] -h [help]


Note: it is important to write path as /home/user/Documents/Annotation_pipeline/Data/
