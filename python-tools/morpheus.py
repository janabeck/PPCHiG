# This Python file uses the following encoding: utf-8

"""
morpheus.py
Created 2011/10/17
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import codecs
import sys

from BeautifulSoup import BeautifulStoneSoup

class Morpheus():
    """A class that transforms Packard-style morphological tags into Penn-style POS tags."""

    def __init__(self):
        pass

def main():

    try:
        in_name1 = sys.argv[1]
	# e.g., gospels-database.xml
        xml_file = codecs.open(in_name1, "rU", "utf-8")
        soup = BeautifulStoneSoup(xml_file)
        words = soup.findAll('word')

        in_name2 = sys.argv[2]
	# e.g., proiel-regexp-map.txt
        regexp_file = codecs.open(in_name2, "rU", "utf-8")

	in_name3 = sys.argv[3]
	# e.g., proiel-GNT-lemma-map.txt
	lemma_file = codecs.open(in_name3, "rU", "utf-8")

	out_name = sys.argv[4]
	out_file = codecs.open(out_name, "w", "utf-8")

	# a list of tuples containing the word-lemma pair and the full Packard morphological tag
	packards = []

	# loop fills packards
	for word in words:
		try:
			# creates the canonical word-lemma pair
			word_lemma = word.string + "-" + word['lemma']
			# creates the full Packard tag as found in the regexp map, e.g., A-_-s---mac-i	ADJR
			packard = word['proiel-pos'] + "_" + word['morph']
			packards.append((word_lemma, packard))
		except KeyError:
			pass
		
	# list of the PROIEL POS tags not handled by regular expressions
	# probably not necessary
	done_by_lemma = ["C-", "Dq", "Du", "G-"]
	
	# list of the PROIEL POS tags only handled partially by regular expressions
	done_part_by_lemma = ["Pd", "Pi", "Pp", "Pr", "Px"]

	# dictionary where key = full Packard tag and value = Penn POS tag
	equivs = {}

	# loop fills equivs 
	for line in regexp_file:
		pair = line.split()
		equivs[pair[0]] = pair[1]

	lem_equivs = {}

	# dictionary where key = tuple of PROIEL POS, lemma and value = Penn POS tag
	for line in lemma_file:
		triple = line.split()
		lem_equivs[(triple[0], triple[1])] = triple[2]

	# list of tuples containing word-lemma, Penn POS tag
	penns = []

	# loop fill penns
	for packard in packards:
		pair = packard[0].split("-")
		lemma = pair[1]
		proiel_pos = packard[1][:2]
		lem_key = (proiel_pos, lemma)
		if packard[1] in equivs:
			penns.append((packard[0], equivs[packard[1]]))
		elif lem_key in lem_equivs:
			# work here! this part isn't getting triggered
			if proiel_pos in done_part_by_lemma:
				penns.append((packard[0], lem_equivs[lem_key] + packard[1]))
			else:
				penns.append((packard[0], lem_equivs[lem_key]))

	for penn in penns:
		print >> out_file, penn[0] + "\t" + penn[1]

    except IndexError:
        print "Usage: python morpheus.py + input XML database file + POS map file + lemma map file + name of output file."
        print
        print "Please try again."
        print

if __name__ == "__main__":
    main()
