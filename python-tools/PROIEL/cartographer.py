# This Python file uses the following encoding: utf-8

"""
cartographer.py
Created 2011/10/17
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com

This program is based on my old chicago_map.py.
"""

import re, sys

def main():
    """Generates a POS map file based on regular expressions for use with morpheus.py."""

    try:
        # file containing the regular expressions that define the translation from the Packard tags to Penn-style POS tags
        # e.g., chicago-herodotus-map.txt
        re_name = sys.argv[1]
        re_file = open(re_name, "rU")

        # file containing a list of all the unique Packard morphological tags in the corpus
        # e.g., HDT-unique-morph-list.txt
        morph_name = sys.argv[2]
        morph_file = open(morph_name, "rU")

        out_name = sys.argv[3]
        out_file = open(out_name, "w")

        guide = {}

        # list of the Chicago POS tags not handled by regular expressions
        done_by_lemma = ["c-","g-"]

        for line in re_file:
            if not line.startswith("#") and not line.isspace():
                info = line.split()
                guide[info[0]] = info[1]

        map_lines = set([])

        for line in morph_file:
            for key in guide:
                if re.match(key, line):
                    new_line = line.rstrip() + "\t" + guide[key]
                    break
                else:
                    if not line[:2] in done_by_lemma:
                        new_line = line.rstrip() + "\tU"
            map_lines.add(new_line)

        for line in map_lines:
            print >> out_file, line
        
    except IndexError:
        print "Usage: python cartographer.py + regular expressions file + unique morph tags file + name of output file."
        print
        print "Please try again."
        print

if __name__ == "__main__":
    main()
