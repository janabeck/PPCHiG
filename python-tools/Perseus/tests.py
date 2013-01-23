from unittest import TestCase
from seeker import Seeker, Token

class TreeTestCase(TestCase):
	"""Test that dependency trees are getting mapped correctly."""

	def runTest(self):

		s = Seeker('test/unit_test.xml')

		hand_dict = {
		'1': [[1,7,8,9,10,11,12,13,14,15,16,17,18],False],
		'2': [[2],True],
		'3': [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],True],
		'4': [[4],True],
		'5': [[4,5,6],True],
		'6': [[6],True],
		'7': [[7], True],
		'8': [[8],True],
		'9': [[9],True],
		'10': [[10],True],
		'11': [[10,11],True],
		'12': [[8,9,10,11,12,13,14,15,16,17,18],True],
		'13': [[13],True],
		'14': [[13,14,15,16,17,18],True],
		'15': [[15],True],
		'16': [[16],True],
		'17': [[15,16,17],True],
		'18': [[15,16,17,18],True],
		'19': [[19],True]
		}

		for tree in s.trees.values():
			for key in tree:
				self.assertEqual(tree[key], hand_dict[key])

def main():
	test = TreeTestCase()
	test.runTest()

if __name__ == '__main__':
	main()