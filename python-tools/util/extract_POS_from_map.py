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

def main():

    map_file = codecs.open(sys.argv[1], "rU", "utf-8")

    out_file = codecs.open("pos_tags.txt", "w", "utf-8")

    tags = set([])

    for line in map_file:
        pair = line.split()
        tags.add(pair[1])

    for tag in tags:
        print >> out_file, tag

if __name__ == "__main__":
    main()
