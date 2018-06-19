# storjStats
A work in progress for analyzing Storj log files in python.

# dependencies
storjStats is intended to function with Python3.5, but may also work with previous version.

Numpy and Pandas are required to run the scripts in storjStats.

# Setup
After installing the dependencies, download a clone of the project, and it can be run one of two ways.
1. Manually run the main.py script with in a linux shell
2. Set up a chron job to run the main.py at a desired interval (avoid around midnight to 2am as this is when the reaper runs)

# Current State
Currently storjStats in intended to work with the linux version of storjShare.  It will run through the log file folder, read the files and pull out the relevant information.  These lines will then be digested in terms of what your farmer node is doing. <b> All information is stored from the farmers perspective. </b>  In other words, if it says upload, that means your node uploaded a file to the internet, if it says download, then you downloaded the file.  This is done in an effort to show exactly what the farmer node is doing in reference to your own bandwidth usage.

This information is sent to a .csv file in the outputs folder in the same directory of the storjStats folder.  Each time storjStats will runs it will read the current .csv file and then pick up from where it left off with a little overlap to make sure it does not miss any action in the log files.  If there is now .csv file in the outputs folder, or if you would like to start fresh just remove the .csv file and storjStats will run through all of the log files present in the log folder.  All dates that are saved as in UTC time.

# Future State
My next development task will be to make some nice graphics with the data that is being stored in the .csv file.  

# Patience
This my first public project, so please have patience as I do this in my off-time.  I appreciate any constructive criticism on my coding or project setup!  I hope you enjoy, and if you don't find this useful, then thanks for stopping by and know I that had fun putting this together.
