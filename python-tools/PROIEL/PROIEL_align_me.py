# This Python file uses the following encoding: utf-8

"""
PROIEL_align_me.py
Created 2011/10/13
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

from BeautifulSoup import BeautifulStoneSoup

import sys
# for Unicode support
import codecs

def main():
    in_name = sys.argv[1]

    in_file = codecs.open(in_name, "rU")

    print "Parsing the XML file with BeautifulStoneSoup..."
    print
    
    soup = BeautifulStoneSoup(in_file)

    print "Finding all the tokens..."
    print
    
    tokens = soup.findAll('token')

    out_file = codecs.open("proiel-gnt.wds", "w", "utf-8")

    for token in tokens:
    # easier to ask forgiveness than permission!
        try:
            print >> out_file, token['id'] + "\t" + token['form']
        except KeyError:
            pass

if __name__ == "__main__":
    main()
