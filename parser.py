#!/usr/bin/env python

import sys
import os
import argparse
import pprint
from libparser import parse_csv

class DefaultHelpParser(argparse.ArgumentParser):
	def error(self, message):
		sys.stderr.write('error: {}\n'.format( message))
		self.print_help()
		sys.exit(2)


if __name__ == "__main__":	
	parser = DefaultHelpParser()
	required = parser.add_argument_group('required arguments')
	required.add_argument('-c', '--csv', dest='input_files', nargs='+',
		help='One or more CSV files to be parsed. If it is a folder the entire folder will be parsed.')
	
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	argparse_arguments = parser.parse_args()

	for file in argparse_arguments.input_files:
		if os.path.isdir(file):
			for subdir_file in os.listdir(file):
				if os.path.isfile(subdir_file):
					print(subdir_file)
					table = parse_csv(subdir_file)
					pprint.pprint(table)
					print('')
		else:
			print(file)
			table = parse_csv(file)
			pprint.pprint(table)
			print('')