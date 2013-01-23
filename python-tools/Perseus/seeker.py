import argparse
from lxml import etree

class Token():
	"""A Perseus dependency tree."""

	def __init__(self):

		self.id = ""

		self.dependencies = {}

class Seeker():
	"""Utility for searching the Perseus Ancient Greek Dependency Treebanks."""

	RE = dict(re="http://exslt.org/regular-expressions")

	def __init__(self, xml_name):

		self.doc = etree.parse(xml_name)

		# temp variable for returning recursive list of a head's dependents
		# kind of a klugey solution, tbh
		self.tmp = []

		self.sentences = self.doc.xpath("//sentence/@id")

		self.trees = {}

		for token in self.sentences:
			tok = Token()
			tok.id = token
			self._map_tree(token, tok)
			self.trees[token] = tok.dependencies

	def _print_all(self):
		"""Print all Token instances."""

		for ident in self.sentences:
			print "Sentence ID #" + ident + ":"
			print self.trees[ident]
			print

	def _map_tree(self, ident, tok):
		"""Map all the dependencies (recursively) in dependency tree with @id = ident."""

		heads = self.doc.xpath("//sentence/word/@id")

		full_tree = {}

		for head in heads:
			dependents = self._get_dependents(ident, head)
			self._turtles(ident, dependents, dependents)
			recurs_deps = self.tmp
			recurs_deps.append(int(head))
			recurs_deps.sort()
			subtree = [recurs_deps]
			subtree.append(self._check_sequence(subtree))
			full_tree[head] = subtree

		tok.dependencies = full_tree

	def _turtles(self, ident, deps, new_deps):
		"""Facilitate recursive getting of dependents."""

		all_next = []

		for idx in new_deps:
			next_level = self._get_dependents(ident, idx)
			if next_level:
				all_next = all_next + next_level

		if all_next:
			deps = deps + all_next
			self._turtles(ident, deps, all_next)
		else:
			self.tmp = deps

	def _get_dependents(self, ident, head):
		"""Return a list of the @ids of the dependents of the @id ('head') passed in."""
		#TODO: This needs to be recursive!

		dependents = self.doc.xpath("//sentence[@id=" + ident + "]/word[@head=" + str(head) + "]/@id")

		return [int(idx) for idx in dependents]

	def _check_sequence(self, head):
		"""Check if all the dependents of (and including) the head are in sequence."""

		last_index = 0

		for index in head[0]:
			if index != last_index + 1 and last_index != 0:
				return False
			last_index = index

		return True

	def get_relation(self, relation, pos_re):
		#TODO: rewrite utilizing Token data structure

		sentence_IDs = self.doc.xpath("//sentence/word[@relation='" + relation + "' and re:test(@postag, '" + pos_re + 
			"')]/../@id", namespaces=self.RE)

		rels = {}

		for ident in sentence_IDs:
			heads = self.doc.xpath("//sentence[@id=" + ident + "]/word[@relation='" + relation + "' and re:test(@postag, '" +
				pos_re + "')]/@id", namespaces=self.RE)

			full_rels = {}

			for head in heads:
				dependents = self._get_dependents(ident, head)
				self._turtles(ident, dependents, dependents)
				recurs_deps = self.tmp
				print "the recursive dependents are: " + str(recurs_deps)
				recurs_deps.append(int(head))
				recurs_deps.sort()
				rel = [recurs_deps]
				rel.append(self._check_sequence(rel))
				full_rels[head] = rel
				print
				print ident, full_rels
				print

			rels[ident] = full_rels

		print rels

def main():

	parser = argparse.ArgumentParser(description='Process the input files.')
	parser.add_argument('-x', '--xml', action = 'store', dest = "xml_name", help='name of Perseus XML file')
	args = parser.parse_args()

	seeker = Seeker(args.xml_name)

	seeker._print_all()

if __name__ == '__main__':
	main()