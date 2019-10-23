# coding=utf-8
# 

import unittest2
from xlrd import open_workbook
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