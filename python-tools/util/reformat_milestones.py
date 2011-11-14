# This Python file uses the following encoding: utf-8

"""
reformat_milestones.py
Created 2011/11/13
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import codecs
import sys
import re

def main():
    """Reformats milestones from (CODE chapter:verse) or (CODE book:chapter:section) format to common (CODE {VS:chapter_verse/section}) format."""

    psd_file = codecs.open(sys.argv[1], "rU", "utf-8")

    out_name = sys.argv[1] + ".new"

    out_file = codecs.open(out_name, "w", "utf-8")

    double = re.compile("(.*\(CODE )([0-9]+?):([0-9]+?)\)")
    triple = re.compile("(.*\(CODE )([0-9]+?):([0-9]+?):([0-9]+?)\)")

    tri = False

    for line in psd_file:
        if line.find(":") != -1:
            if double.match(line):
                blah = double.match(line)
                pre = blah.group(1)
                num1 = "{VS:" + blah.group(2) + "_"
                num2 = blah.group(3) + "})\n"
                line = pre + num1 + num2
            elif triple.match(line):
                Tri = True
                blah = triple.match(line)
                pre = blah.group(1)
                num1 = "{VS:" + blah.group(3) + "_"
                num2 = blah.group(4) + "})\n"
                line = pre + num1 + num2

        print >> out_file, line,
            
if __name__=="__main__":
    main()
