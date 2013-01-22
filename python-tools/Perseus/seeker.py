import argparse
from lxml import etree

class Seeker():
	"""Utility for searching the Perseus Ancient Greek Dependency Treebanks."""

	RE = dict(re="http://exslt.org/regular-expressions")

	def __init__(self, xml_name):

		self.doc = etree.parse(xml_name)

	def get_relation(self, relation, pos_re):

		sentence_IDs = self.doc.xpath("//sentence/word[@relation='" + relation + "' and re:test(@postag, '" + pos_re + 
			"')]/../@id", namespaces=self.RE)

		rels = {}

		for ident in sentence_IDs:
			heads = self.doc.xpath("//sentence[@id=" + ident + "]/word[@relation='" + relation + "' and re:test(@postag, '" +
				pos_re + "')]/@id", namespaces=self.RE)

			full_rels = {}

			for head in heads:
				dependents = self.get_dependents(ident, head)
				dependents.append(int(head))
				dependents.sort()
				rel = [dependents]
				rel.append(self.check_sequence(rel))
				full_rels[head] = rel

			rels[ident] = full_rels

		print rels

	def get_dependents(self, ident,head):
		"""Return a list of the @ids of the dependents of the @id ('head') passed in."""
		#TODO: This needs to be recursive!

		dependents = self.doc.xpath("//sentence[@id=" + ident + "]/word[@head=" + head + "]/@id")

		return [int(ident) for ident in dependents]

	def check_sequence(self, head):
		"""Check if all the dependents of (and including) the head are in sequence."""

		last_index = 0

		for index in head[0]:
			if index != last_index + 1 and last_index != 0:
				return False
			last_index = index

		return True

def main():

	parser = argparse.ArgumentParser(description='Process the input files.')
	parser.add_argument('-x', '--xml', action = 'store', dest = "xml_name", help='name of Perseus XML file')
	args = parser.parse_args()

	seeker = Seeker(args.xml_name)

	seeker.get_relation('OBJ', 'n-.---.a-')

if __name__ == '__main__':
	main()