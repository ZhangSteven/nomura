# coding=utf-8
#
# Read Nomura holding anc cash reports, convert them to Geneva holding and cash
# format.
# 

from xlrd import open_workbook
from itertools import takewhile, chain
from functools import partial
from utils.excel import worksheetToLines
from utils.utility import fromExcelOrdinal, dictToValues, writeCsv
from utils.iter import pop
from nomura.utility import getCurrentDirectory
from os.path import join
import logging
logger = logging.getLogger(__name__)




"""
	[Dictionary] p (raw holding position) => 
		[Dictionary] Geneva holding position
"""
holdingPosition = lambda date, folder, p: \
	{ 'portfolio': folder + '_nomura'\
	, 'custodian': ''\
	, 'date': date\
	, 'geneva_investment_id': ''\
	, 'ISIN': p['Isin']\
	, 'bloomberg_figi': ''\
	, 'name': p['Security Name']\
	, 'currency': p['Security Issue CCY']\
	, 'quantity': p['TD Quantity']\
	}



"""
	[Dictionary] p (raw cash position) => 
		[Dictionary] Geneva cash position
"""
cashPosition = lambda date, folder, p: \
	{ 'portfolio': folder + '_nomura'\
	, 'custodian': ''\
	, 'date': date\
	, 'currency': p['Currency']\
	, 'balance': p['SD Balance Local']\
	}



"""
	[Iterable] lines => [String] date, [Iterable] Positions

	Read the lines from a Nomura position or cash report, return date and
	positions from that report.
"""
getPositions = lambda file: \
	(lambda lines: (dateFromLine(pop(lines)), getRawPositions(lines)))\
	(fileToLines(file))



"""
	[Iterable] lines => ([List] headers, [Iterable] lines)

	Take the first line and convert it to headers, then return the
	headers and the remaining lines.

	This is NOT a pure function. The first line of lines is consumed.
"""
getHeadersnLines = lambda lines: \
	( list(takewhile(lambda x: x != '', map(lambda x: x.strip(), pop(lines))))\
	, lines\
	)



"""
	[Iterable] lines => [Iterable] Positions

	lines: rows in a file, where each row is a list of columns

	Assume the first line is column headers
"""
getRawPositions = lambda lines: \
	(lambda headers, lines: \
		map( lambda line: dict(zip(headers, line))\
		   , takewhile( lambda line: not line[0].startswith('Record Count')\
			  		  , lines))
	)(*getHeadersnLines(lines))



"""
	[String] file => [Iterable] lines

	Read an Excel file, convert its first sheet into lines, each line is
	a list of the columns in the row.
"""
fileToLines = lambda file: \
	worksheetToLines(open_workbook(file).sheet_by_index(0))



"""
	[List] line => [String] date (yyyy-mm-dd)

	First item in the line is the date. Most of the time the date is
	read a float number, but sometimes it is read as a string (dd/mm/yyyy)
"""
dateFromLine = lambda line: \
	(lambda x: \
		fromExcelOrdinal(x).strftime('%Y-%m-%d') \
		if isinstance(x, float) else \
		(lambda items: \
			items[2] + '-' + items[1] + '-' + items[0]
		)(x.split('/'))
	)(line[0])



isCashFile = lambda fn: \
	fn.split('\\')[-1].startswith('Cash Stt')



folderFromFilename = lambda fn: \
	(lambda s: '_'.join(s.split()))(fn.split('\\')[-2])



getCashHeaders = lambda: \
	['portfolio', 'custodian', 'date', 'currency', 'balance']



getHoldingHeaders = lambda: \
	[ 'portfolio', 'custodian', 'date', 'geneva_investment_id'\
	, 'ISIN', 'bloomberg_figi', 'name', 'currency', 'quantity'\
	]



getOutputFileName = lambda inputFile, postfix, outputDir: \
	join(outputDir, folderFromFilename(inputFile) + postfix + '.csv')



toOutputData = lambda inputFile: \
	(lambda date, positions: \
		( '_' + date + '_cash'\
		, chain( [getCashHeaders()]\
			   , map( partial(dictToValues, getCashHeaders())\
			   		, map( partial(cashPosition, date, folderFromFilename(inputFile))\
			   			 , positions)))\
		) if isCashFile(inputFile) else \

		( '_' + date + '_position'\
		, chain( [getHoldingHeaders()]\
			   , map( partial(dictToValues, getHoldingHeaders())\
			   		, map( partial(holdingPosition, date, folderFromFilename(inputFile))\
			   			 , positions)))\
		)
	)(*getPositions(inputFile))



outputCsv = lambda inputFile, outputDir: \
	(lambda postfix, outputData: \
		writeCsv( getOutputFileName(inputFile, postfix, outputDir)\
				, outputData, delimiter='|')
	)(*toOutputData(inputFile))




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	# inputFile = join(getCurrentDirectory(), 'samples', 'Cash Stt _22102019.xlsx')
	inputFile = join(getCurrentDirectory(), 'samples', 'Holding _22102019.xlsx')
	print(outputCsv(inputFile, ''))