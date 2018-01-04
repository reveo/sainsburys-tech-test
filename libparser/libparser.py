import json
import pprint
import logging

from collections import namedtuple
from logging.config import fileConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

week_days = ['mon', 'tue', 'wed', 'thu', 'fri']
square_days = week_days[:3]
double_days = week_days[3:]


def process_file(filename):
	"""
	reads the first 2 lines of a csv file, first line the header, 2nd line for the data
	releated to the header. The header and the data contains instructions for the parser
	how to generate data. Header and data should have the same length
	:param filename: the name of he csv file
	:return: a tuple containing the header and the data
	"""
	logger.debug("{}".format(__name__))

	with open(filename, 'r') as f:
		inp = []
		for line in f:
			inp.append(line)
		header = inp[0]
		data = inp[1]
	return (header, data)


def unfold_header(header, data):
	"""
	Expand header range values and map them to the data provided, for example mon-wed will
	become mon, tue, wed and the corresponding data will be repeated as many times
	as the length of the expanded list.
	:param header: the header to be prcessed
	:param data: related data to he header
	:return: tuple with the expanded header and data
	"""
	logger.debug("{}".format(__name__))

	expanded_header = []
	expanded_data = []
	for h, d in zip(header.split(','), data.split(',')):
		if '-' not in h:
			expanded_header.append(h)
			expanded_data.append(d)
		else:
			left_day, right_day = map(str, h.split('-'))
			left_day_index = 0; right_day_index = 0;
			for index, day in enumerate(week_days):
				if day == left_day:
					left_day_index = index
				if day == right_day:
					right_day_index = index		
			expanded_header.extend(week_days[left_day_index: right_day_index + 1])
			# Be careful when the item being repeated is a list. d is a scalar not a list!! or we would end up with [[], [], []]
			expanded_data.extend([d] * (right_day_index - left_day_index + 1))

			"""
			Other possible way is using generators, would make sense if the result is more than one, and then we could use next() on the result to iterate through
			the above solution is clearer in our case
			left_day_index = 
				list((index for index, day in enumerate(week_days) if day == left_day))[0]
			right_day_index = 
				list((index for index, day in enumerate(week_days) if day == right_day))[0]		
			"""	
	logger.debug("expanded_header: {}".format(expanded_header))
	logger.debug("expanded_data: {}".format(expanded_data))
	return (expanded_header, expanded_data)


def process_calculation(expanded_header, expanded_data):
	"""
	Dispatch lambdas, perform calculations on the data as per the instructions
	:param expanded_header: the expanded_header from the unfold function
	:param expanded_data: the expanded_data from the unfold function
	:return: tuple with the data_collection, which is the expanded header and the calculations together,
	description which is the description field.
	"""
	logger.debug("{}".format(__name__))

	dispatch = {
		'square': lambda x: x**2,
		'double': lambda x: x*2
	}

	# perform calculations required, square and double for specific days
	Data = namedtuple('Data', ['day', 'operation', 'value', 'operation_value'])
	desc = ""
	data_collection = []
	for h, d in zip(expanded_header, expanded_data):		
		try:		
			# throws an exception so except clause will be executed if its not an int. 
			# Assumption is that days have integer data, anything else have string data		
			val_d = int(d)		

			if h in square_days:							
				op = 'square'				
			if h in double_days:				
				op = 'double'
			
			"""
			Could be done this way, but we have no spec what to do if the calc is missing
			op = 'square' if h in square_days else 'double' if h in double_days else ''
			if op == '':
				# TODO: log the error, we have no specification what to do in this case
				pass				
			"""
			data = Data(day=h, operation=op, value=val_d, operation_value=dispatch[op](val_d))	
			data_collection.append(data)	

		except:
			h = h.strip()
			if h == 'description':
				desc = d.strip()

	logger.debug("data_collection: {}".format(data_collection))
	logger.debug("description: {}".format(desc))
	return (data_collection, desc)


def unfold_data(data_collection, desc):
	"""
	Function to generate the data set to be returned from the parser, we generate this in one
	go instead of using a generator and yield which would be more suitable for large datasets so that
	we are not loading the entire dataset into memory but use an iterator instead.
	:param data_collection: the data collection to process
	:param desc: the description field which is needed to process some of the fields in the collection
	:return: the data set generated.
	"""
	# process data for output
	logger.debug("{}".format(__name__))

	table = []
	for data in data_collection:

		row = { 
			'day': data.day, 
			'description': ' '.join((desc, str(data.operation_value))),
			 data.operation: data.operation_value,
			'value': data.value  }
		table.append(row)

	logger.debug("table: {}".format(table))
	return table

def parse_csv(file):
	# parse csv
	logger.debug("{}".format(__name__))

	(header, data) = process_file(file)
	(expanded_header, expanded_data) = unfold_header(header, data);
	(data_collection, desc) = process_calculation(expanded_header, expanded_data)
	return unfold_data(data_collection, desc)
	

