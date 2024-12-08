The run_auto-tests Docker image performs the following operations:

1) Downloads the metadata.json file located in the pegi3s project folder /dockerfiles/metadata to /opt (within the Docker image) and prepares from it a new JSON that is appropriate to run the auto-tests (get_json.py)
2) Retrieves the test data located on evolution6 for the tests to be performed and saves it to a folder named "input_data" under /data (the working directory). If the test data already exists in /data/input_data this step is skipped (retrieve_test_data.py)
3) Performs the tests by (run_docker.py):
	a) removing the Docker image being tested if it exists locally
	b) running the tests, which implies pulling the image given the previous step - succes is measured by:
	    i) for CLI images, the creation of a designated output file with non-zero size
		ii) for GUI images, the ability to close the Docker image, meaning that it was running
4) Removing the tested Docker image to avoid cluttering

The output message stating whether the test run with scuccess or not is:

1) displayed on the console
2) written to the log file under /data (the working directory)

It looks like:

"On the 08/12/2024, it took 16.46 seconds to successfully execute pegi3s/muscle:3.8.31."		

In order to use the run_auto-tests Docker image you must provide two files in the working directory:

1) a file (hereafter named "tests_to_run" but that may have any name) listing the tests to be run one per line (the mandatory test has the same name as the Docker image name)
2) since we are running Docker in Docker, a config file (hereafter named "config" but that may have any name) with the structure: dir=/your/data/dir

Then use the command:

docker run -v /your/data/dir:/data -v /var/run/docker.sock:/var/run/docker.sock pegi3s/run_auto-tests bash -c "python3 main.py tests_to_run config"

This is a small list of tests that run with success and that you can use for your own tests:

clustalomega
seda
mafft
muscle
coral
probcons_nuc
tcoffee
cutadapt
evoppi-querier
jmodeltest2
alter
bedtools
graphviz
sratoolkit
bioconvert
flash
entrez-direct
getpdb
goalign
gotree
id-mapping
abyss
edena
plottree
wgsim
omegamap
newick_utils
probcons
raxml
tm-align_server
phipack
picard
plasflow
check-cds