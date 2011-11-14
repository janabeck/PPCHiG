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

    in_file = codecs.open("herodotus.xml", "rU", "utf-8")

    print "Parsing the input file with BeautifulStoneSoup..."
    print

    soup = BeautifulStoneSoup(in_file)

    print "Finding all the tokens..."
    print

    tokens = soup.findAll('w')

    out_file = codecs.open("HDT-morph-list.txt", "w", "utf-8")

    out_file2 = codecs.open("HDT-pos-list.txt", "w", "utf-8")

    unique_tags = Set([])

    short_tags = Set([])

    for token in tokens:
        try:
            tag = token['pos']
            if tag != "":
                unique_tags.add(tag)
                short_tag = tag[:2]
                short_tags.add(short_tag)
            
        except KeyError:
            pass
    
    for tag in unique_tags:
        print >> out_file, tag

    for tag in short_tags:
        print >> out_file2, tag
    
if __name__ == "__main__":
    main()
