# This Python file uses the following encoding: utf-8

"""
break_tokens.py
Created 2011/11/16
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

## This program has NOT been modified for new corpus formatting standards!
## DO NOT USE!

import re
import string
import codecs
import sys

def main():
    """Break and re-number tokens."""
    
    corpus = raw_input("What corpus are you working on?\n\
    (This is the part of the ID before the comma.) ")
    print

    in_name = raw_input("What is the name of your input file minus the file extension? ")
    print

    inputFile = in_name + ".psd"

    outputFile = in_name + ".psd.new"
    
    input = codecs.open(inputFile, "r", "utf-8").readlines()    

    output = codecs.open(outputFile, "w", "utf-8")

    index = 1

    old_book = ""

    for line_num, line in enumerate(input):
        i0 = string.find(line, "<+")
        ID = string.find(line, "(ID " + corpus)
        if i0 != -1:
            # when a line contains "<+", either break the token or make into a comment
            i1 = string.find(line, "<+ IP")
            i2 = string.find(line, "<+ CP")
            i3 = string.find(line, "<+ FRAG")
            if (i1 != -1 or i2 != -1 or i3 != -1):
                # when the comments contain IP, CP, or FRAG, break tokens
                #print line
                m = re.match('^\s*(.*)\s<\+\s(.*)\s\+>$', line)
                try:
                    partialLine = m.group(1)
                    #print partialLine
                    tokenType = m.group(2)
                    #print tokenType
                    print >> output, partialLine + ")\n  (ID " + corpus + "," + book + "." + str(index) + "))\n\n( (" + tokenType + " ",
                except AttributeError:
                    print "The comment on line " + str(line_num+1) + " is not in the correct format!"
                    print "Fix and start over!"
                    sys.exit()
                index = index + 1
            else:
                # when the comments are just comments, enclose in (CODE {COM:...})
                #print line
                m2 = re.match('^\s*(.*)\s<\+\s(.*)\s\+>$', line)
                beginningOfLine = m2.group(1)
                comment = m2.group(2)
                comment2 = re.sub('\s', '_', comment)
                comment3 = re.sub(':', '=', comment2)
                print >> output, beginningOfLine + "\n" + "(CODE {" + comment3 + "})"
        elif ID != -1:
            # when a line contains "(ID [corpus]", renumber it
            bk = re.match('^\s*\(ID [A-Za-z]+,([A-Za-z0-9]+)\.[0-9a-z]+\)\)$', line)
            book = bk.group(1)
            if old_book != book:
                index = 1
            newLine = '  (ID ' + corpus + ',' + book + '.' + str(index) + '))'
            old_book = book
            print >> output, newLine
            index = index + 1
        else:
            print >> output, line,

if __name__ == "__main__":
    main()
