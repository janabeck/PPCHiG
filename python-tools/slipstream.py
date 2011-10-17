# This Python file uses the following encoding: utf-8

"""
slipstream.py
Created 2011/10/13
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

from BeautifulSoup import BeautifulStoneSoup, Tag, NavigableString

import codecs

def main():
    """Create an XML database containing a word from the GNT, its PROIEL ID # and other PROIEL info."""

    aligned = codecs.open("aligned-matthew.wds", "rU", "utf-8")

    xml = codecs.open("proiel-matthew.xml", "rU", "utf-8")

    print "Parsing the PROIEL XML with BeautifulStoneSoup..."
    print

    proiel = BeautifulStoneSoup(xml)

    tokens = proiel.findAll('token')

    tok_dict = {}

    # creating a dictionary keyed by PROIEL IDs to speed up searching
    for token in tokens:
        tok_dict[token['id']] = token

    output = open("gnt-database.xml", "w")

    print >> output, "<div>"

    print >> output, "<title>Matthew</title>"

    count = 100001

    soup = BeautifulStoneSoup()

    word = Tag(soup, "word")

    print "Iterating through the alignment file..."
    print

    for line in aligned:
        stuff = line.split("\t")
        word = Tag(soup, "word")
        form = NavigableString(stuff[0])
        word.insert(0, form)
        # make it so that the IDs count up from 000000, not 100000
        word['id'] = str(count).replace("1", "0", 1)
        word['proiel-id'] = stuff[1]

        # adding attributes from the PROIEL XML
        if stuff[1] != "000000" and stuff[1] != "999999" and stuff[1] != "111111":
            token = tok_dict[stuff[1]]
            morph = token['morph-features'].split(",")
            word['lemma'] = morph[0]
            word['proiel-pos'] = morph[1]
            word['lang'] = morph[2]
            word['morph'] = morph[3]
            word['deprel'] = token['relation']
            try:
                word['proiel-head-id'] = token['head-id']
            except KeyError:
                word['proiel-head-id'] = "root"
            
        word['proiel-form'] = stuff[2].rstrip()
        count += 1
        print >> output, word

    print >> output, "</div>"

    print "Done!"
    print

if __name__ == "__main__":
    main()
