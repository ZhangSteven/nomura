# coding=utf-8
# 

import unittest2
from xlrd import open_workbook
from utils.iter import firstOf
from os.path import join
from nomura.utility import getCurrentDirectory
from nomura.main import getPositions, toOutputData, getCashHeaders\
						, getHoldingHeaders



class TestALL(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestALL, self).__init__(*args, **kwargs)



	def testRawPosition(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'Holding _22102019.xlsx')
		dt, positions = (lambda t: (t[0], list(t[1])))(getPositions(inputFile))
		self.assertEqual('2019-10-22', dt)
		self.assertEqual(48, len(positions))
		self.verifyRawPosition(firstOf( lambda p: p['Security Name'] == 'EASY TACTIC LTD 9.125% 28/07/2022'\
									  , positions))



	def testCashRawPosition(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'Cash Stt _22102019.xlsx')
		dt, positions = (lambda t: (t[0], list(t[1])))(getPositions(inputFile))
		self.assertEqual('2019-10-22', dt)
		self.assertEqual(1, len(positions))
		self.verifyCashRawPosition(positions[0])



	def testOutputData(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'Holding _22102019.xlsx')
		postfix, data = (lambda t: (t[0], list(t[1])))(toOutputData(inputFile))
		self.assertEqual('_2019-10-22_position', postfix)
		self.assertEqual(49, len(data))
		self.assertEqual(getHoldingHeaders(), data[0])
		self.verifyOutputLine(firstOf( lambda line: line[4] == 'XS1640517907'\
									 , map(list, data)))



	def testOutputData2(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'Holding _24102019.xlsx')
		postfix, data = (lambda t: (t[0], list(t[1])))(toOutputData(inputFile))
		self.assertEqual('_2019-10-24_position', postfix)
		self.assertEqual(49, len(data))
		self.assertEqual(getHoldingHeaders(), data[0])
		self.verifyOutputLine2(firstOf( lambda line: line[4] == ''\
									  , map(list, data)))



	def testOutputData3(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'Cash Stt _22102019.xlsx')
		postfix, data = (lambda t: (t[0], list(t[1])))(toOutputData(inputFile))
		self.assertEqual('_2019-10-22_cash', postfix)
		self.assertEqual(2, len(data))
		self.assertEqual(getCashHeaders(), data[0])
		self.verifyOutputLine3(list(data[1]))



	def testOutputData3(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'Holding _24102019.xlsx')
		postfix, data = (lambda t: (t[0], list(t[1])))(toOutputData(inputFile))
		self.assertEqual('_2019-10-24_position', postfix)
		self.assertEqual(49, len(data))



	def verifyRawPosition(self, position):
		"""
		EASY TACTIC LTD 9.125% 28/07/2022
		"""
		self.assertEqual(37, len(position))
		self.assertEqual('XS1940202952', position['Isin'])
		self.assertEqual('USD', position['Security Issue CCY'])
		self.assertEqual(530000, position['TD Quantity'])



	def verifyCashRawPosition(self, position):
		"""
		The only USD position
		"""
		self.assertEqual(14, len(position))
		self.assertEqual('USD', position['Currency'])
		self.assertEqual(3177773.5, position['SD Balance Local'])



	def verifyOutputLine(self, line):
		"""
		Output data items:

		portfolio|custodian|date|geneva_investment_id|ISIN|
		bloomberg_figi|name|currency|quantity
		"""
		self.assertEqual('samples_nomura', line[0])
		self.assertEqual('', line[1])
		self.assertEqual('2019-10-22', line[2])
		self.assertEqual('', line[3])
		self.assertEqual('XS1640517907', line[4])
		self.assertEqual('', line[5])
		self.assertEqual('21VIANET GROUP INC 7% 17/08/2020', line[6])
		self.assertEqual('USD', line[7])
		self.assertEqual(2000000, line[8])



	def verifyOutputLine2(self, line):
		"""
		The special case: XS1684793018

		Output data items:

		portfolio|custodian|date|geneva_investment_id|ISIN|
		bloomberg_figi|name|currency|quantity
		"""
		self.assertEqual('samples_nomura', line[0])
		self.assertEqual('', line[1])
		self.assertEqual('2019-10-24', line[2])
		self.assertEqual('XS1684793018_Bond', line[3])
		self.assertEqual('', line[4])
		self.assertEqual('', line[5])
		self.assertEqual('POSTAL SAVINGS BANK OF CHINA CO LTD FRN', line[6])
		self.assertEqual('USD', line[7])
		self.assertEqual(3000000, line[8])



	def verifyOutputLine3(self, line):
		"""
		Output data items

		portfolio|custodian|date|currency|balance
		"""
		self.assertEqual('samples_nomura', line[0])
		self.assertEqual('', line[1])
		self.assertEqual('2019-10-22', line[2])
		self.assertEqual('USD', line[3])
		self.assertEqual(3177773.5, line[4])