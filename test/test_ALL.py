# coding=utf-8
# 

import unittest2
from xlrd import open_workbook
from utils.iter import firstOf
from os.path import join
from nomura.utility import getCurrentDirectory
from nomura.main import getPositions



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