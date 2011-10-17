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
        in_file1 = codecs.open(in_name1, "rU", "utf-8")
        soup = BeautifulStoneSoup(in_file1)
        words = soup.findAll('word')

        in_name2 = sys.argv[2]
        in_file2 = codecs.open(in_name2, "rU", "utf-8")

    except IndexError:
        print "Usage: python morpheus.py + input XML file + POS map file + lemma map file."
        print
        print "Please try again."
        print

if __name__ == "__main__":
    main()
