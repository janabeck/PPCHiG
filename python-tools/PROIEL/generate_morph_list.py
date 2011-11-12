# This Python file uses the following encoding: utf-8

"""
generate_morph_list.py
Created 2011/10/17
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import re
import codecs

from BeautifulSoup import BeautifulStoneSoup

from sets import Set

def main():
    """Generate a list of all the morphological tags in an XML document."""

    in_file = codecs.open("proiel-GNT.xml", "rU", "utf-8")

    print "Parsing the input file with BeautifulStoneSoup..."
    print

    soup = BeautifulStoneSoup(in_file)

    print "Finding all the tokens..."
    print

    tokens = soup.findAll('token')

    out_file = codecs.open("GNT-morph-list.txt", "w", "utf-8")

    unique_tags = Set([])

    for token in tokens:
        try:
            stuff = token['morph-features'].split(",")
            proiel_pos = stuff[1]
            proiel_morph = stuff[3]
            tag = proiel_pos + "_" + proiel_morph
            unique_tags.add(tag)
        except KeyError:
            pass
    
    for tag in unique_tags:
        print >> out_file, tag
    
if __name__ == "__main__":
    main()
