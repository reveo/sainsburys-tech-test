import pytest
from collections import namedtuple
from libparser.libparser import (
	process_file,
	unfold_header,
	process_calculation,
	unfold_data
	)


@pytest.fixture()
def header(request):
	headers = dict([
		(1, 'mon,tue,some_column1,wed,thu,fri,description'), 
		(2, 'mon-thu,fri,description,another_column2'),
		(3, 'some_data,mon-tue,wed-thu,fri,description')
	])
	return headers[request.param]
	

@pytest.fixture()
def data(request):
	datas = dict([ 
		(1, '1,5,data,2,3,3,first_desc'), 
		(2, '2,3,second_desc,some_data'),
		(3, ',3,2,1,third_desc')])
	return datas[request.param]
			

@pytest.fixture()
def expected(request):
	expected_output = dict([
		(1, [{'day': 'mon', 'description': 'first_desc 1', 'square': 1, 'value': 1},
		{'day': 'tue', 'description': 'first_desc 25', 'square': 25, 'value': 5},
		{'day': 'wed', 'description': 'first_desc 4', 'square': 4, 'value': 2},
		{'day': 'thu', 'description': 'first_desc 6', 'double': 6, 'value': 3},
		{'day': 'fri', 'description': 'first_desc 6', 'double': 6, 'value': 3}]),

		(2, [{'day': 'mon', 'description': 'second_desc 4', 'square': 4, 'value': 2},
		 {'day': 'tue', 'description': 'second_desc 4', 'square': 4, 'value': 2},
		 {'day': 'wed', 'description': 'second_desc 4', 'square': 4, 'value': 2},
		 {'day': 'thu', 'description': 'second_desc 4', 'double': 4, 'value': 2},
		 {'day': 'fri', 'description': 'second_desc 6', 'double': 6, 'value': 3}]),

		(3,  [{'day': 'mon', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 		{'day': 'tue', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 		{'day': 'wed', 'description': 'third_desc 4', 'square': 4, 'value': 2},
 		{'day': 'thu', 'description': 'third_desc 4', 'double': 4, 'value': 2},
 		{'day': 'fri', 'description': 'third_desc 2', 'double': 2, 'value': 1}]
 		)])
	return expected_output[request.param]


@pytest.fixture()
def csv_data_file(request):	
	TestData = namedtuple('TestData', ['header', 'data'])
	with open(request.param, 'r') as f:
		inp = []
		for line in f:
			inp.append(line)
		
		return TestData(header=inp[0], data=inp[1])


@pytest.mark.parametrize('header, data, expected', [(1,1,1), (2,2,2), (3,3,3)], indirect=True)
def test_parser(header, data, expected):	
	(expanded_header, expanded_data) = unfold_header(header, data);
	(data_collection, desc) = process_calculation(expanded_header, expanded_data)
	assert unfold_data(data_collection, desc) == expected
	

@pytest.mark.parametrize('csv_data_file, expected', [('1.csv', 1), ('2.csv', 2), ('3.csv', 3)], indirect=True)
def test_parser_input_csv(csv_data_file, expected):			
	(expanded_header, expanded_data) = unfold_header(csv_data_file.header, csv_data_file.data);
	(data_collection, desc) = process_calculation(expanded_header, expanded_data)
	table = unfold_data(data_collection, desc)		
	assert table == expected
 	