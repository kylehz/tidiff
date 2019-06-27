import unittest
import util

same = util.same

class TestSolution(unittest.TestCase):
	def test1(self):
		self.assertEquals(same(
			{"port" : 4000}, {"port" : 5000}),
			(False, {'port': (4000, 5000)}))
	def test2(self):
		self.assertEquals(same(
			{"port" : 4000, "report-status" : True}, {"port" : 4000}),
			(False, {'report-status': (True, None)}))
	def test3(self):
		self.assertEquals(same(
			{"port" : 4000, "status" : {}}, {"port" : 4000, "status" : { "report-status" : True}}),
			(False, {'status': {'report-status': (None, True)}}))

if __name__ == '__main__':
    unittest.main()