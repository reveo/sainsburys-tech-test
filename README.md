Sainsbyrys Technical Test

Getting Started

1. Prerequisites
You need Python 3 and Virtualenv on your machine

2. Setup<

To run the parser go into the folder where you have downloaded or copied the project. Create a virtualenv called venv in the application directory, activate the virtualenv and install required dependencies using pip.

$ cd /path/to/sainsburys-test/
$ pyvenv-3.6 env
$ source env/bin/activate
$ pip install -r requirements.txt

3. Running the parser

**Examples**

**Parse a single file**
(venv) $ python parser.py -c 1.csv

**Expected output**
1.csv
[{'day': 'mon', 'description': 'first_desc 1', 'square': 1, 'value': 1},
 {'day': 'tue', 'description': 'first_desc 25', 'square': 25, 'value': 5},
 {'day': 'wed', 'description': 'first_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'first_desc 6', 'double': 6, 'value': 3},
 {'day': 'fri', 'description': 'first_desc 6', 'double': 6, 'value': 3}]

**Parse multiple files**
(venv) $ python parser.py -c 1.csv 2.csv 3.csv

**Parse an enire directory**
(venv) $ python parser.py -c csv_files

**Parse an enire directory and a single file**
(venv) $ python parser.py -c csv_files 1.csv


4. Running the tests

To run the test suite simply execute
(venv) $ pytest


Enjoy!