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
        re_name = sys.argv[1]
        re_file = open(re_name, "rU")

        morph_name = sys.argv[2]
        morph_file = open(morph_name, "rU")

        out_name = sys.argv[3]
        out_file = open(out_name, "w")

        guide = {}

        for line in re_file:
            if not line.startswith("#")
                info = line.split()
                guide[info[0]] = info[1]
        
        for line in morph_file:
            for key in guide:
                if re.match(key, line):
                    line = line.rstrip() + "\t" + guide[key]
                    print >> out_file, line                
        
    except IndexError:
        print "Usage: python morpheus.py + regular expressions file + unique morph tags file + name of output file."
        print
        print "Please try again."
        print

if __name__ == "__main__":
    main()
