# This Python file uses the following encoding: utf-8

"""
chicago_scrubber.py
Created 2012/01/22
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

from BeautifulSoup import BeautifulStoneSoup, Comment

import sys
import re
import codecs

from perseus_scrubber import Scrub

class ChicagoScrub(Scrub):

    def parse(self):
        """Parses the raw XML of the input file."""

        print "Parsing raw XML file using BeautifulStoneSoup..."
        print

        # initial parse
        soup = BeautifulStoneSoup(self.in_file, selfClosingTags=['milestone', 'ref'])

        print "Finished parsing raw XML using BeautifulStoneSoup."
        print

        out_name = self.to_scrub
        self.open_out(out_name)
        
        print "Finding major divisions in the XML file..."
        print
        
        # gets sub-trees for all books
        divisions = soup.findAll(type="book")
        book = 1
        for division in divisions:
            self.scrub(division, book)
            book += 1
            if book == 2:
                break

    def scrub(self, division, book):
        """Scrubs the XML in the division passed to it to prep the content for output."""

        print "Scrubbing and formatting XML..."
        print

        chapter = 0
        section = 0

        # stores the body of the sub-tree of interest
        para = division.find('p')

        # removes comments, i.e., <!-- note resp="ed"...
        comments = para.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]

        self.filter(para, chapter, section)

    def filter(self, node, chapter, section):

        for item in node.contents:
            try:
                if item.name == "w":
                    if item["lemma"] !+ "":
                        pair = "(X " + item.string + "-" + "lemma" + ")"
                    else:
                        pair = "(X " + item.string + "-" + item["lemma"] + ")"
                    self.text.append(pair)
                    self.count += 1
                elif item.name == "milestone":
                    if item['unit'] == "chapter":
                        chapter = item['n']
                    elif item['unit'] == "section":
                        section = item['n']
                        self.text.append("(CODE {VS:" + str(chapter) + "_" + str(section) + "})")
                elif item.name == "quote":
                    self.filter(item, chapter, section)
                elif item.name == "l":
                    self.filter(item, chapter, section)
                elif item.name == "ref":
                    pass
                else:
                    print "Uh oh! I found something else!"
                    print
                    print "This element is " + item.name
                    print
                    sys.exit()
            # catches punctuation
            except AttributeError:
                tag = ""
                if not item.isspace():
                    for ch in item:
                        if ch != "":
                            if ch.strip() == "(":
                                ch = "LPAREN"
                            elif ch.strip() == ")":
                                ch = "RPAREN"
                            elif ch.strip() == u"”":
                                tag = "\""
                            elif ch.strip() == u"“":
                                tag = "\""
                            if tag != "":
                                pair = "(" + tag + " " + ch.rstrip() + "-" + ch.rstrip() + ")"
                                tag = ""
                            else:
                                pair = "(" + ch.rstrip() + " " + ch.rstrip() + "-" + ch.rstrip() + ")"
                            if pair != "( -)":
                                self.text.append(pair)

    def load(self):
        """Opens the raw XML file."""
        
        self.in_file = codecs.open(self.to_scrub, "rU", "utf-8")

        print "Opening raw XML file..."
        print

    def open_out(self, out_name):
        """Opens a file for output."""

        out_name = out_name.replace(".xml",".pos")

        self.out_file = codecs.open(out_name, "w", "utf-8")

    def output(self):
        """Prints each item in the list to the output file."""

        print "Printing to " + self.out_file.name + "..."
        print
        
        print >> self.out_file, "((IP-MAT "
        
        length = len(self.text)
        count = 0

        open_quote = u"“"

        close_quote = u"”"

        in_quote = False

        for item in self.text:
            if open_quote in item:
                in_quote = True
            if in_quote:
                if not close_quote in item:
                    print >> self.out_file, item
                    count += 1
                else:
                    in_quote = False
                    new_item = item + ")"
                    print >> self.out_file, new_item
                    print >> self.out_file, "(ID Herodotus,Histories.0))"
                    count += 1
                    if count < length:
                        print >> self.out_file, "((IP-MAT "
            else:
                if not "(. " in item:
                    print >> self.out_file, item
                    count += 1
                else:
                    new_item = item + ")"
                    print >> self.out_file, new_item
                    print >> self.out_file, "(ID Herodotus,Histories.0))"
                    count += 1
                    if count < length:
                        print >> self.out_file, "((IP-MAT "

        print "This file has " + str(self.count) + " words."

def main():
    
    book = ChicagoScrub()

    book.output()
    
if __name__ == "__main__":
    main()
