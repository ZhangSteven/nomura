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



# toOutputData = lambda inputFile: \
# 	(lambda date, positions: \
# 		( date + '_cash'
# 		, chain( [getCashHeaders()]\
# 			   , map( partial(dictToValues, getCashHeaders())\
# 			   		, map(cashPosition, positions)))\
# 		)\
# 	)(*getPositions(inputFile)) \
	
# 	if isCashFile(inputFile) else \
	
# 	(lambda date, positions: \
# 		( date + '_position'
# 		, chain( [getHoldingHeaders()]\
# 			   , map( partial(dictToValues, getHoldingHeaders())\
# 			   		, map(holdingPosition, positions)))\
# 		)\
# 	)(*getPositions(inputFile))



def toOutputData(inputFile):
	date, positions = getPositions(inputFile)
	if isCashFile(inputFile):
		return   '_' + date + '_cash'\
			   , chain( [getCashHeaders()]\
			   		  , map( partial(dictToValues, getCashHeaders())\
			   			   , map( partial(cashPosition, date, folderFromFilename(inputFile))\
			   			   		, positions)))

	else:
		return   '_' + date + '_position'\
			   , chain( [getHoldingHeaders()]\
			   		  , map( partial(dictToValues, getHoldingHeaders())\
			   			   , map( partial(holdingPosition, date, folderFromFilename(inputFile))\
			   			   		, positions)))



def outputCsv(inputFile, outputDir):
	"""
	[String] inputFile, [String] outputDir
	"""
	postfix, outputData = toOutputData(inputFile)

	return writeCsv( getOutputFileName(inputFile, postfix, outputDir)\
				   , outputData\
				   , delimiter='|'\
			       )




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	inputFile = join(getCurrentDirectory(), 'samples', 'Cash Stt _22102019.xlsx')
	print(outputCsv(inputFile, ''))