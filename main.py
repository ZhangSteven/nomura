# coding=utf-8
#
# Read Nomura holding anc cash reports, convert them to Geneva holding and cash
# format.
# 

from xlrd import open_workbook
from itertools import takewhile
from utils.excel import worksheetToLines
from utils.utility import fromExcelOrdinal
from utils.iter import pop
from nomura.utility import getCurrentDirectory
import logging
logger = logging.getLogger(__name__)



"""
	[Iterable] lines => [String] date, [Iterable] Positions

	Read the lines from a Nomura position or cash report, return date and
	positions from that report.
"""
getPositions = lambda file: \
	(lambda lines: (dateFromLine(pop(lines)), getRawPositions(lines)))\
	(fileToLines(file))



def getRawPositions(lines):
	"""
	[Iterable] lines => [Iterable] Positions

	lines: rows in a file, where each row is a list of columns

	Assume the first line is column headers
	"""
	headers = list(takewhile( lambda x: x != ''\
					  		, map(lambda x: x.strip(), pop(lines))))

	return map( lambda line: dict(zip(headers, line))\
			  , takewhile( lambda line: not line[0].startswith('Record Count')\
			  			 , lines))



"""
	[String] file => [Iterable] lines

	Read an Excel file, convert its first sheet into lines, each line is
	a list of the columns in the row.
"""
fileToLines = lambda file: \
	worksheetToLines(open_workbook(file).sheet_by_index(0))



"""
	[List] line => [String] date (yyyy-mm-dd)

	First line in Nomura holding or cash report
"""
dateFromLine = lambda line: \
	fromExcelOrdinal(pop(line)).strftime('%Y-%m-%d')




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	from os.path import join
	inputFile = join(getCurrentDirectory(), 'samples', 'Cash Stt _22102019.xlsx')
	_, cash = getPositions(inputFile)
	for x in cash:
		print(x)