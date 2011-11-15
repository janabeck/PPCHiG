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

def main():

    try:
        in_name1 = sys.argv[1]
	# e.g., gospels-database.xml
        xml_file = codecs.open(in_name1, "rU", "utf-8")
        soup = BeautifulStoneSoup(xml_file)
        words = soup.findAll('w')

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
            # creates the canonical word-lemma pair
            if word['lemma'] != "":
                word_lemma = word.string + "-" + word['lemma']
            else:
                word_lemma = word.string + "-lemma"
            # creates the full Packard tag as found in the regexp map, e.g., A-_-s---mac-i	ADJR
            if word['pos'] != "":
                packard = word['pos']
            else:
                packard = "X"
            packards.append((word_lemma, packard))
				
	# list of the PROIEL POS tags not handled by regular expressions
	# probably not necessary
	done_by_lemma = ["c-", "g-"]
	
	# list of the PROIEL POS tags only handled partially by regular expressions
	done_part_by_lemma = ["d-", "dr", "pd", "pi", "pp", "pr"]

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
            wd = pair[0]
            proiel_pos = packard[1][:2]
            lem_key = (proiel_pos, lemma)
            if wd != "lacuna":
                # first condition: 1
                if packard[1] in equivs:
                    # 1a
                    if lem_key in lem_equivs:
                        if proiel_pos in done_part_by_lemma:
                            if not proiel_pos.startswith("p"):
                                tmp = lem_equivs[lem_key]
                            else:
                                tmp = lem_equivs[lem_key] + equivs[packard[1]]
                                tmp = tmp.replace("nom.sing", "")
                                tmp = tmp.replace("gen.sing", "$")
                                tmp = tmp.replace("acc.sing", "A")
                                tmp = tmp.replace("dat.sing", "D")
                                # D is the only Penn POS tag in the done_part_by_lemma that distinguishes singular from plural
                                if lem_equivs[lem_key] == "D":
                                    tmp = tmp.replace("nom.pl", "S")
                                    tmp = tmp.replace("gen.pl", "S$")
                                    tmp = tmp.replace("acc.pl", "SA")
                                    tmp = tmp.replace("dat.pl", "SD")
                                # PRO, WPRO, ADJ, WADJ, Q, etc. don't distinguish singular from plural
                                else:
                                    tmp = tmp.replace("nom.pl", "")
                                    tmp = tmp.replace("gen.pl", "$")
                                    tmp = tmp.replace("acc.pl", "A")
                                    tmp = tmp.replace("dat.pl", "D")
                            penns.append((packard[0], tmp))
                    # 1b
                    else:
                        penns.append((packard[0], equivs[packard[1]]))
                # 2
                elif lem_key in lem_equivs:
                    penns.append((packard[0], lem_equivs[lem_key]))
                # 3
                else:
                    penns.append((packard[0], packard[1]))

	for penn in penns:
	    print >> out_file, penn[0] + "\t" + penn[1]

    except IndexError:
        print "Usage: python morpheus.py + input XML database file + POS map file + lemma map file + name of output file."
        print
        print "Please try again."
        print

if __name__ == "__main__":
    main()
