#!/bin/bash
#Data_Path=/home/rhuang06/Documents/Annotation_pipeline/Data
#Obo_Path=/home/rhuang06/Documents/Annotation_pipeline/go-basic.obo
#Out_Path=/home/rhuang06/Documents/Annotation_pipeline

#echo -e "\nPlease provide the path of folder of data\n"

#read Data_Path

#echo -e "\nPlease provide the path of folder for saving processed data\n"

#read Out_Path



echo -e "###############################################################################"
echo -e "# Automatic gene annotation pipeline for animal genome via comparative genomics"
echo -e "###############################################################################\n"

script_path=`pwd`



cd ../

Out_Path=`pwd`

python_version=python3.6

while :
do
	echo -e "\nDo you wish to download go-basic.obo file? (yes/no)\n"
	read answer
	case $answer in
		"yes")
			echo -e "\nDownloading file\n"
			cd $Out_Path
			wget http://purl.obolibrary.org/obo/go/go-basic.obo
			break
			;;
		"no")
			echo -e "\nPlease provide path of go-basic.obo\n"
			read obo
			break
			;;
		*)
		echo -e "\nPlease enter yea or no\n"
		;;
	esac
done

if [ -z "$obo" ];then
	Obo_Path=$Out_Path/go-basic.obo
else
	Obo_Path=$obo
fi

echo -e "\nCheck if needed libraries are installed in python\n"

if ! command -v pip3
then
    echo -e "\npip3 is not found\nTry to install pip3\n"
	sudo apt-get install python3-pip
	if [ $? -ne 0 ];then
		echo -e "\nFail to instal pip\n"
		echo -e "\nPlease see readme file for solution\n"
		exit 1
	fi
fi

if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("pandas"))'; then
	echo -e '\npandas found\n'
else
	echo -e "\ninstalling pandas\n"
	sudo pip3 install pandas
		if [ $? -ne 0 ];then
		echo -e "\nFail to instal pandas\n"
		exit 1
	fi
fi

if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("numpy"))'; then
	echo -e '\nnumpy found\n'
else
	echo -e "\ninstalling numpy\n"
	sudo pip3 install numpy
			if [ $? -ne 0 ];then
		echo -e "\nFail to instal numpy\n"
		exit 1
	fi
fi

if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("argparse"))'; then
	echo -e '\nargparse found\n'
else
	echo -e "\ninstalling argparse\n"
	sudo pip3 install argparse
			if [ $? -ne 0 ];then
		echo -e "\nFail to instal argparse\n"
		exit 1
	fi
fi

if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("difflib"))'; then
	echo -e '\ndifflib found\n'
else
	echo -e "\ninstalling difflib\n"
	sudo pip3 install difflib
			if [ $? -ne 0 ];then
		echo -e "\nFail to instal difflib\n"
		exit 1
	fi
fi


if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("csv"))'; then
	echo -e '\ncsv found\n'
else
	echo -e "\ninstalling csv\n"
	sudo pip3 install csv
			if [ $? -ne 0 ];then
		echo -e "\nFail to instal csv\n"
		exit 1
	fi
fi

if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("pybiomart"))'; then
	echo -e '\npybiomart found\n'
else
	echo -e "\ninstalling pybiomart\n"
	sudo pip3 install pybiomart
			if [ $? -ne 0 ];then
		echo -e "\nFail to instal pybiomart\n"
		exit 1
	fi
fi

if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("multiprocessing"))'; then
	echo -e '\nmultiprocessing found\n'
else
	echo -e "\ninstalling multiprocessing\n"
	sudo pip3 install multiprocessing
			if [ $? -ne 0 ];then
		echo -e "\nFail to instal multiprocessing\n"
		exit 1
	fi
fi

if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("pickle"))'; then
	echo -e '\npickle found\n'
else
	echo -e "\ninstalling pickle\n"
	sudo pip3 install pickle
			if [ $? -ne 0 ];then
		echo -e "\nFail to instal pickle\n"
		exit 1
	fi
fi

if $python_version -c 'import pkgutil; exit(not pkgutil.find_loader("shutil"))'; then
	echo -e '\nshutil found\n'
else
	echo -e "\ninstalling shutil\n"
	sudo pip3 install shutil
			if [ $? -ne 0 ];then
		echo -e "\nFail to instal shutil\n"
		exit 1
	fi
fi

#Data folder path
Data_Path=$Out_Path/Data

#Processed data folder path
table_path=$Out_Path/Proccessed_Data

#Path for same gene script
same_path=$table_path/ORTH

#clique input file one to one file
clique_file=$table_path/Fuse_Orth_file/Final_Cliquer_one_file.txt

#Result folder
result_folder=$Out_Path/Results/

cd $script_path

echo -e "\n##################################\n"

echo -e "Start Downloading Ensembl data"

#$python_version Ensembl_download.py -outpath $Out_Path/

echo -e "\n##################################\n"

echo -e "Start data pre-processing"

echo -e "\n##################################\n"

$python_version data_preparation.py -obo $Obo_Path -path $Data_Path -outpath $Out_Path

echo -e "\nProcessed files are saved in $table_path"


echo -e "\n##################################\n"

echo -e "Processed data are located in Proccessed_Data file"

echo -e "\n###################################\n"

echo -e "\nStart detecting if gene name of each pair of orthologue are same or different\n"

$python_version detect_same_or_different_gene.py -path $same_path -outpath $Out_Path

echo -e "\nProducing statistical data\n"

$python_version Generate_Statistics.py -path $table_path -outpath $Out_Path

echo -e "\nStatistical txt file is saved in $Out_Path\n"

echo -e "\nTry to fuse Ortholog files\n"

$python_version Fuse_Ortholog.py -path $table_path -outpath $Out_Path

echo -e "\nProducing index file and removing repeated ortholog relations\n"

$python_version Index_file_Reduced_orth_file.py -path $same_path -outpath $Out_Path

echo -e "\nFiles are saved in $Out_Path /Fuse_Orth_file\n"

echo -e "\nProducing ACSII file for cliquer\n"

$python_version Cliquer_file.py -path $same_path -outpath $Out_Path

echo -e "\nFile is saved in $Out_Path /Fuse_Orth_file\n"

echo -e "\nRunning cliquer .... \n"

#cliquer -a -m 3 $clique_file > ../Results/cliquer_output_for_Final_Cliquer_one_file_size_3-8_sorted.txt

echo -e "\ncliquer process finished \n"

echo -e "\nProcessing cliquer outputs \n"

if [ ! -d ../Results ]; then
  mkdir ../Results
fi

cd ../Results

grep size=8 cliquer_output_for_Final_Cliquer_one_file_size_3-8_sorted.txt > size8.txt
grep size=7 cliquer_output_for_Final_Cliquer_one_file_size_3-8_sorted.txt > size7.txt
grep size=6 cliquer_output_for_Final_Cliquer_one_file_size_3-8_sorted.txt > size6.txt
grep size=5 cliquer_output_for_Final_Cliquer_one_file_size_3-8_sorted.txt > size5.txt
grep size=4 cliquer_output_for_Final_Cliquer_one_file_size_3-8_sorted.txt > size4.txt
grep size=3 cliquer_output_for_Final_Cliquer_one_file_size_3-8_sorted.txt > size3.txt

if [ ! -d ./sep_size ]; then
  mkdir ./sep_size
fi



mv size* ./sep_size

cd ./sep_size
mv ./size8.txt ../

split -d -l 20000 size7.txt size7_
split -d -l 20000 size6.txt size6_
split -d -l 20000 size5.txt size5_
split -d -l 50000 size4.txt size4_
split -d -l 50000 size3.txt size3_

rm *.txt

cd ../../scripts

echo -e "\nPRocess finish\n"

echo -e "\nStart gene annontation enrichment for cow\n"

$python_version Clique_filtering_GO_scoring.py -path $result_folder -outpath $Out_Path/

echo -e "Process finished"

echo -e "**********************Process finished**********************"


