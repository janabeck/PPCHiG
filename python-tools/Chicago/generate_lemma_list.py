# This Python file uses the following encoding: utf-8

"""
generate_lemma_list.py
Created 2011/10/17
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import codecs

from sets import Set

from BeautifulSoup import BeautifulStoneSoup

def main():
    """Print a list of all the lemmas that have a certain proiel-pos tag in the database."""

    in_file = codecs.open("herodotus.xml", "rU", "utf-8")

    print "Parsing the input file with BeautifulStoneSoup..."
    print

    soup = BeautifulStoneSoup(in_file)

    print "Finding all the tokens..."
    print

    tokens = soup.findAll('w')

    # e.g., dd,de,di,dr,dx,c-,p-,pa,pc,pd,pi,pk,pp,pr,ps,px,m-,i-,e-,g-,gm
    tag_list = raw_input("What Chicago POS tags do you want to find all the lemmas for? Enter these as a comma-separated list. ")
    print

    tags = tag_list.split(",")

    out_file = codecs.open("HDT-lemma-list.txt", "w", "utf-8")
    
    for tag in tags:

        lemmas = Set([])
        
        for token in tokens:
            try:
                if token['pos'].startswith(tag):
                    lemma = token['lemma']
                    lemmas.add(lemma)
            except KeyError:
                pass

        print >> out_file, "The lemmas for tag " + tag + " are: "
        print >> out_file

        for lemma in lemmas:
            print >> out_file, lemma

        print >> out_file
        
if __name__ == "__main__":
    main()
