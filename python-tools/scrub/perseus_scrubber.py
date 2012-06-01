"""
perseus_scrubber.py
Created 2012/01/22
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

from BeautifulSoup import BeautifulStoneSoup, Comment, Tag, NavigableString

try:
    from lxml import etree
except ImportError:
    print "Error importing etree from lxml..."
from tauber import Trie
import sys
import re
import codecs

class Scrub:
    """A class for parsing Perseus Digital Library raw XML files and generating various types of output."""
    
    def __init__(self):
        """Initialize input and output file objects, as well as a dictionary of everything from the input file
        that should be printed."""

        self.to_scrub = sys.argv[1]
        print
        self.in_file = None
        self.out_file = None
        self.text = []
        self.count = 0
        self.pretty = False
        self.english = False
        self.convert_cts = False
        self.load()
        self.parse()

    def parse(self):
        """Parses the raw XML of the input file."""
        chapter = 0
        verse = 0

        # creates the parse tree from the input file
        print "Parsing raw XML file using BeautifulStoneSoup..."
        print

        # initial parse
        soup = BeautifulStoneSoup(self.in_file)

        print "Now that the raw XML has been parsed, you have several options for output:"
        print "\ta. One word per line, punctuation and milestones included (for checking against parsed files)."
        print "\tb. Pretty text for printing and/or reading. (Under construction.)"
        print "\tc. C(anonical)T(ext)S(ervices)-compliant XML. (Under construction.)"
        print

        choice = raw_input("Please type the letter of your output choice: ")
        print
        
        if choice == "a":
            choice2 = raw_input("Do you want to output the entire document? Please type y or n. ")
            print
            if choice2 == "y":
                out_name = self.to_scrub
                # gets sub-trees for all books
                divisions = soup.findAll(type="Book")
                for division in divisions:
                    self.scrub(division)
                self.open_out(out_name)
                self.output()
            if choice2 == "n":
                out_name = raw_input("What book do you want to scrub? ")
                print
                # stores the sub-tree of interest
                division = soup.find(n=out_name)
                self.scrub(division)
                self.open_out(out_name)
                self.output()
        if choice == "b":
            self.pretty = True
            eng = raw_input("Are you scrubbing an English document? Answer with y or n. ")
            print
            self.english = True
            choice2 = raw_input("Do you want to output the entire document? Please type y or n. ")
            print
            if choice2 == "y":
                out_name = raw_input("What would you like to name the output file? (It will be given a .txt extension.) ")
                # gets sub_trees for all books
                divisions = soup.findAll(type="Book")
                for division in divisions:
                    self.scrub(division)
                self.open_out(out_name)
                self.output()
            if choice2 == "n":
                out_name = raw_input("What book do you want to output? ")
                print
                # stores the sub-tree of interest
                division = soup.find(type="Book", n=out_name)
                self.scrub(division)
                self.open_out(out_name)
                self.output()
        if choice == "c":
            self.convert_cts = True
            out_name = raw_input("What book do you want to convert to CTS-conformant XML? ")
            print
            # stores the sub-tree of interest
            division = soup.find(n=out_name)
            self.cts(soup, division)
        
    def scrub(self, division):
        """Scrubs the XML in the division passed to it to prep the content for output."""

        # stores the body of the sub-tree of interest
        para = division.find('p')
        
        print "Extracting comments..."
        print
        # removes comments, i.e., <!-- note resp="ed"...
        comments = para.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
        
        print "Scrubbing..."
        print

        for item in para.contents:
            try:
                # records and formats milestones
                if item.name == "milestone":
                    if item['unit'] == "chapter":
                        chapter = item['n']
                    elif item['unit'] == "verse" or item['unit'] == "section":
                        verse = item['n']
                        milestone = "(CODE " + str(chapter) + ":" + str(verse) + ")"
                        self.text.append(milestone.rstrip())
                        for n in item.contents:
                            if n.string:
                                self.tokenize(n.string)
                            elif n.name == "name":
                                self.tokenize(n.contents[0].string)
                    elif item['unit'] == "para":
                        for n in item.contents:
                            if n.string:
                                self.tokenize(n.string)
                            elif n.name == "name":
                                self.tokenize(n.contents[0].string)                                
                # extracts text from name and placeName nodes
                elif item.name == "name":
                    if item['type'] == "place":
                        print item.contents[0].string
                        self.tokenize(item.contents[0].string)
                    else:
                        self.tokenize(item.string)
                # extracts text from <quote> nodes
                elif item.name == "quote":
                    for node in item.contents:
                        try:
                            if node.name == "l":
                                for leaf in node.contents:
                                    try:
                                        if leaf.name == "milestone":
                                            if leaf['unit'] == "chapter":
                                                chapter = leaf['n']
                                            if leaf['unit'] == "verse":
                                                verse = leaf['n']
                                                milestone = "(CODE " + str(chapter) + ":" + str(verse) + ")"
                                                self.text.append(milestone.rstrip())
                                        if leaf.name == "name":
                                            if leaf['type'] == "place":
                                                self.tokenize(leaf.contents[0].string)
                                            else:
                                                self.tokenize(leaf.string)
                                    except AttributeError:
                                        if not leaf.isspace():
                                            self.tokenize(leaf)
                            elif node.name == "milestone":
                                if node['unit'] == "chapter":
                                    chapter = node['n']
                                if node['unit'] == "verse":
                                    verse = node['n']
                                    milestone = "(CODE " + str(chapter) + ":" + str(verse) + ")"
                                    self.text.append(milestone.rstrip())
                            elif node.name == "name":
                                if item['type'] == "place":
                                    self.tokenize(item.contents[0].string)
                                else:
                                    self.tokenize(item.string)
                        except AttributeError:
                            try:
                                if not node.isspace():
                                    self.tokenize(node)
                            except TypeError:
                                print "(Caught in quote block.) This node is of type " + node.name + ". Would you like to continue?"
                                answer = raw_input("Please type y or n. ")
                                if answer == "y":
                                    pass
                                if answer == "n":
                                    sys.exit()
                # extracts text from <q> nodes
                elif item.name == "q":
                    for node in item.contents:
                        try:
                            if node.name == "l":
                                for leaf in node.contents:
                                    try:
                                        if leaf.name == "milestone":
                                            if leaf['unit'] == "chapter":
                                                chapter = leaf['n']
                                            if leaf['unit'] == "verse":
                                                verse = leaf['n']
                                                milestone = "(CODE " + str(chapter) + ":" + str(verse) + ")"
                                                self.text.append(milestone.rstrip())
                                        elif leaf.name == "quote":
                                            for shoot in leaf.contents:
                                                try:
                                                    if shoot.name == "milestone":
                                                        if shoot['unit'] == "chapter":
                                                            chapter = shoot['n']
                                                        if shoot['unit'] == "verse":
                                                            verse = shoot['n']
                                                            milestone = "(CODE " + str(chapter) + ":" + str(verse) + ")"
                                                            self.text.append(milestone.rstrip())
                                                except AttributeError:
                                                    if not shoot.isspace():
                                                        self.tokenize(shoot)
                                    except AttributeError:
                                        if not leaf.isspace():
                                            self.tokenize(leaf)
                            elif node.name == "milestone":
                                if node['unit'] == "chapter":
                                    chapter = node['n']
                                elif node['unit'] == "verse":
                                    verse = node['n']
                                    milestone = "(CODE " + str(chapter) + ":" + str(verse) + ")"
                                    self.text.append(milestone.rstrip())
                            elif node.name == "quote":
                                for leaf in node.contents:
                                    try:
                                        if leaf.name == "l":
                                            self.tokenize(leaf.string)
                                        elif leaf.name == "milestone":
                                            if leaf['unit'] == "chapter":
                                                chapter = leaf['n']
                                            elif leaf['unit'] == "verse":
                                                verse = leaf['n']
                                                milestone = "(CODE " + str(chapter) + ":" + str(verse) + ")"
                                                self.text.append(milestone.rstrip())
                                    except AttributeError:
                                        if not leaf.isspace():
                                            self.tokenize(leaf)
                        except AttributeError:
                            if not node.isspace():
                                self.tokenize(node)
                elif item.string:
                    self.tokenize(item.string)
            # an exception occurs when the node is a NavigableText object (i.e., a block of text)
            except AttributeError:
                try:
                    if not item.isspace():
                        self.tokenize(item.string)
                except TypeError:
                    print "This node is of type " + item.name + ". Would you like to continue?"
                    answer = raw_input("Please type y or n. ")
                    if answer == "y":
                        if item.name == "name":
                            if item['type'] == "place":
                                self.tokenize(item.contents[0].string)
                            else:
                                self.tokenize(item.string)
                    if answer == "n":
                        sys.exit()
                        
    def cts(self, soup, division):
        """Generates CTS-conformant XML from the raw Perseus XML."""
        
        out_name = division['n'].lower() + "_gk.xml"
        
        self.out_file = codecs.open(out_name, "w", "utf-8")
        
        template = open("nt_template.xml", "rU")
        
        new_soup = etree.parse(template)

        book = NavigableString(division['n'])
        
        root = new_soup.getroot()
        
        head = root.getchildren()[0]
        
        fs = head.getchildren()[0]
        
        ts = fs.getchildren()[0]

        title = etree.Element('title')
        
        title.text = book
        
        ts.append(title)

        source_name = division['n'] + ".wmp"
                
        current_wmp = codecs.open(source_name, "rU", "utf-8")
        
        ch = re.compile("\(CODE (\d+):")
        
        vs = re.compile(":(\d+)\)")
        
        milestone = re.compile("\(CODE \d+:\d+\)")
        
        current_chapter = "1"

        text = root.getchildren()[1]
        
        bdy = text.getchildren()[0]
        
        div = etree.Element("div", n="1", type="chapter")
        
        p = etree.SubElement(div, "p")
        
        bdy.append(div)
        
        seg = etree.Element("seg", n="1", type="verse")

        current_string = ""
        
        print "Converting text..."
        print
        
        first_verse = False
        
        for line in current_wmp:
            if line == "(CODE 1:1)\n":
                continue
            elif milestone.search(line):
                if ch.search(line):
                    chapter = ch.search(line).group(1)
                    if chapter != current_chapter:
                        seg.text = current_string
                        p.append(seg)
                        div = etree.Element("div", n=chapter, type="chapter")
                        p = etree.SubElement(div, "p")
                        bdy.append(div)
                        current_chapter = chapter
                        first_verse = True
                    elif chapter == current_chapter:
                        first_verse = False
                if vs.search(line):
                    if not first_verse:
                        seg.text = current_string
                        p.append(seg)
                        verse = vs.search(line).group(1)
                        seg = etree.Element("seg", n=verse, type="verse")
                        current_string = ""
                    if first_verse:
                        verse = vs.search(line).group(1)
                        seg = etree.Element("seg", n=verse, type="verse")
                        current_string = ""
            elif "." in line or "," in line or ";" in line or ":" in line:
                current_string = current_string.rstrip() + line.rstrip() + " "
            else:
                current_string = current_string + line.rstrip() + " "
        
        seg.text = current_string
        p.append(seg)
        
        sys.stdout = self.out_file
        
        print etree.tostring(new_soup, encoding=unicode)
        
        sys.stdout = sys.__stdout__

        print "Conversion completed."
        print

    def load(self):
        """Opens the raw XML file."""

        self.in_file = open(self.to_scrub, "rU")

        print "Opening raw XML file..."
        print

    def open_out(self, out_name):
        """Opens a file for output."""
        
        if not self.pretty:
            out_name = out_name + ".wmp"
        if self.pretty:
            out_name = out_name + ".txt"
        
        self.out_file = codecs.open(out_name, "w", "utf-8")

    def output(self):
        """Prints each item in the dictionary to the output file."""

        if not self.text:
            exit(0)  

        print "Printing to " + self.out_file.name + "..."
        print
        
        if not self.pretty:
            for item in self.text:
                print >> self.out_file, item

            print "This file has " + str(self.count) + " words."
            print
            
        if self.pretty:
            for item in self.text:
                if "CODE" in item:
                    new = item.replace("(CODE ", "")
                    newer = new.replace(")", "")
                    newer = newer + "\t"
                    print >> self.out_file, "\n\n" + newer,
                else:
                    print >> self.out_file, item,     
                    
        print "Printing completed."
        print

    def tokenize(self, line):
        """Sanitizes the raw text, converts it to unicode, and adds everything to self.text[]."""
        
        bad_char = re.compile('&.*?;')
        
        if not self.pretty:
            # first, some sanitization to remove XML character entity references
            line = line.replace("&lt;*&gt;","")
            line = bad_char.sub("", line)
            
            # second, replace punctuation with space + punctuation so that punctuation ends up as a separate item
            line = line.replace(".", " .")
            line = line.replace(",", " ,")
            line = line.replace(";", " ;")
            line = line.replace(":", " :")
            # changes colons to periods b/c interference with chapter:verse
            #line = line.replace(":", " .")
            # removes brackets
            line = line.replace("[","")
            line = line.replace("]","")
            
        if self.pretty:
            # changes XML character entity references to characters
            #line = line.replace("&lt;*&gt;","<*>")
            # plan to fix the following later to actually sub characters for XML character reference entities
            line = bad_char.sub("", line)
        
        # break string into component words
        l = re.split('\\s', line)
        for item in l:
            # tests for empty strings and ignores them
            if item:
                # only counts non-punctuation as words
                if not (item == "." or item == "," or item == ";" or item == ":"):
                    self.count += 1
                    if self.english:
                        uni_item = item
                    else:
                        # shifts alpha characters to uppercase for beta2unicode
                        upper_item = item.upper()
                        # adds a newline to the end of every item so that final sigmas will show up as such
                        new_item = upper_item + "\n"
                        try:
                            uni_item = unicode(self.beta2uni(new_item), "utf-8")
                        except Exception:
                            print "Beta to unicode error!"
                            print item
                            self.output()
                            sys.exit(1)
                    # adds unicode Greek minus extra newline to the list of items to be printed
                    self.text.append(uni_item.rstrip())
                else:
                    # adds punctuation to the list of items to be printed
                    self.text.append(item)

    def beta2uni(self, item):
        """Modified from the outer scope of J. Tauber's beta2unicode.py."""
        t = self.beta2unicodeTrie()
        
        a, b = t.convert(item)
        if b:
            print a.encode("utf-8")
            raise Exception
        return a.encode("utf-8")
    
    def beta2unicodeTrie(self):
        """Modified (fixed betacode to unicode correspondences or added where lacunas) from J. Tauber's beta2unicode.py."""
        t = Trie()

        t.add("*A",      u"\u0391")
        t.add("*B",      u"\u0392")
        t.add("*G",      u"\u0393")
        t.add("*D",      u"\u0394")
        t.add("*E",      u"\u0395")
        t.add("*Z",      u"\u0396")
        t.add("*H",      u"\u0397")
        t.add("*Q",      u"\u0398")
        t.add("*I",      u"\u0399")
        t.add("*K",      u"\u039A")
        t.add("*L",      u"\u039B")
        t.add("*M",      u"\u039C")
        t.add("*N",      u"\u039D")
        t.add("*C",      u"\u039E")
        t.add("*O",      u"\u039F")
        t.add("*P",      u"\u03A0")
        t.add("*R",      u"\u03A1")
        t.add("*S",      u"\u03A3")
        t.add("*T",      u"\u03A4")
        t.add("*U",      u"\u03A5")
        t.add("*F",      u"\u03A6")
        t.add("*X",      u"\u03A7")
        t.add("*Y",      u"\u03A8")
        t.add("*W",      u"\u03A9")

        t.add("A",      u"\u03B1")
        t.add("B",      u"\u03B2")
        t.add("G",      u"\u03B3")
        t.add("D",      u"\u03B4")
        t.add("E",      u"\u03B5")
        t.add("Z",      u"\u03B6")
        t.add("H",      u"\u03B7")
        t.add("Q",      u"\u03B8")
        t.add("I",      u"\u03B9")
        t.add("K",      u"\u03BA")
        t.add("L",      u"\u03BB")
        t.add("M",      u"\u03BC")
        t.add("N",      u"\u03BD")
        t.add("C",      u"\u03BE")
        t.add("O",      u"\u03BF")
        t.add("P",      u"\u03C0")
        t.add("R",      u"\u03C1")

        t.add("S\n",    u"\u03C2")
        t.add("S,",     u"\u03C2,")
        t.add("S.",     u"\u03C2.")
        t.add("S:",     u"\u03C2:")
        t.add("S;",     u"\u03C2;")
        t.add("S]",     u"\u03C2]")
        t.add("S@",     u"\u03C2@")
        t.add("S_",     u"\u03C2_")
        t.add("S",      u"\u03C3")

        t.add("T",      u"\u03C4")
        t.add("U",      u"\u03C5")
        t.add("F",      u"\u03C6")
        t.add("X",      u"\u03C7")
        t.add("Y",      u"\u03C8")
        t.add("W",      u"\u03C9")

        t.add("I+",     U"\u03CA")
        t.add("U+",     U"\u03CB")

        t.add("A)",     u"\u1F00")
        t.add("A(",     u"\u1F01")
        t.add("A)\\",   u"\u1F02")
        t.add("A(\\",   u"\u1F03")
        t.add("A)/",    u"\u1F04")
        t.add("A(/",    u"\u1F05")
        t.add("E)",     u"\u1F10")
        t.add("E(",     u"\u1F11")
        t.add("E)\\",   u"\u1F12")
        t.add("E(\\",   u"\u1F13")
        t.add("E)/",    u"\u1F14")
        t.add("E(/",    u"\u1F15")
        t.add("H)",     u"\u1F20")
        t.add("H(",     u"\u1F21")
        t.add("H)\\",   u"\u1F22")
        t.add("H(\\",   u"\u1F23")
        t.add("H)/",    u"\u1F24")
        t.add("H(/",    u"\u1F25")
        t.add("I)",     u"\u1F30")
        t.add("I(",     u"\u1F31")
        t.add("I)\\",   u"\u1F32")
        t.add("I(\\",   u"\u1F33")
        t.add("I)/",    u"\u1F34")
        t.add("I(/",    u"\u1F35")
        t.add("O)",     u"\u1F40")
        t.add("O(",     u"\u1F41")
        t.add("O)\\",   u"\u1F42")
        t.add("O(\\",   u"\u1F43")
        t.add("O)/",    u"\u1F44")
        t.add("O(/",    u"\u1F45")
        t.add("U)",     u"\u1F50")
        t.add("U(",     u"\u1F51")
        t.add("U)\\",   u"\u1F52")
        t.add("U(\\",   u"\u1F53")
        t.add("U)/",    u"\u1F54")
        t.add("U(/",    u"\u1F55")
        t.add("W)",     u"\u1F60")
        t.add("W(",     u"\u1F61")
        t.add("W)\\",   u"\u1F62")
        t.add("W(\\",   u"\u1F63")
        t.add("W)/",    u"\u1F64")
        t.add("W(/",    u"\u1F65")

        t.add("A)=",    u"\u1F06")
        t.add("A(=",    u"\u1F07")
        t.add("H)=",    u"\u1F26")
        t.add("H(=",    u"\u1F27")
        t.add("I)=",    u"\u1F36")
        t.add("I(=",    u"\u1F37")
        t.add("U)=",    u"\u1F56")
        t.add("U(=",    u"\u1F57")
        t.add("W)=",    u"\u1F66")
        t.add("W(=",    u"\u1F67")

        t.add("*A)",     u"\u1F08")
        t.add("*)A",     u"\u1F08")
        t.add("*A(",     u"\u1F09")
        t.add("*(A",     u"\u1F09")
        
        t.add("*(\A",    u"\u1F0B")
        t.add("*A)/",    u"\u1F0C")
        t.add("*)/A",    u"\u1F0C")
        t.add("*A(/",    u"\u1F0F")
        t.add("*(/A",    u"\u1F0F")
        t.add("*E)",     u"\u1F18")
        t.add("*)E",     u"\u1F18")
        t.add("*E(",     u"\u1F19")
        t.add("*(E",     u"\u1F19")
        
        t.add("*(\E",    u"\u1F1B")
        t.add("*E)/",    u"\u1F1C")
        t.add("*)/E",    u"\u1F1C")
        t.add("*E(/",    u"\u1F1D")
        t.add("*(/E",    u"\u1F1D")

        t.add("*H)",     u"\u1F28")
        t.add("*)H",     u"\u1F28")
        t.add("*H(",     u"\u1F29")
        t.add("*(H",     u"\u1F29")
        t.add("*H)\\",   u"\u1F2A")
        t.add(")\\*H",   u"\u1F2A")
        t.add("*)\\H",   u"\u1F2A")
        
        t.add("*H)/",    u"\u1F2C")
        t.add("*)/H",    u"\u1F2C")
        
        t.add("*)=H",    u"\u1F2E")
        t.add("(/*H",    u"\u1F2D")
        t.add("*(/H",    u"\u1F2D")
        t.add("*(\\H",   u"\u1F2B")
        t.add("*I)",     u"\u1F38")
        t.add("*)I",     u"\u1F38")
        t.add("*I(",     u"\u1F39")
        t.add("*(I",     u"\u1F39")
        
        t.add("*I)/",    u"\u1F3C")
        t.add("*)/I",    u"\u1F3C")
        
        t.add("*I(/",    u"\u1F3F")
        t.add("*(/I",    u"\u1F3F")

        t.add("*O)",     u"\u1F48")
        t.add("*)O",     u"\u1F48")
        t.add("*O(",     u"\u1F49")
        t.add("*(O",     u"\u1F49")
        
        t.add("*(\O",    u"\u1F4B")
        t.add("*O)/",    u"\u1F4C")
        t.add("*)/O",    u"\u1F4C")
        t.add("*O(/",    u"\u1F4D")
        t.add("*(/O",    u"\u1F4D")
        
        t.add("*U(",     u"\u1F59")
        t.add("*(U",     u"\u1F59")
        
        t.add("*(/U",    u"\u1F5D")
        
        t.add("*(=U",    u"\u1F5F")
        
        t.add("*W)",     u"\u1F68")
        t.add("*)W",     u"\u1F68")
        t.add("*W(",     u"\u1F69")
        t.add("*(W",     u"\u1F69")
        
        t.add("*W)/",    u"\u1F6C")
        t.add("*)/W",    u"\u1F6C")
        t.add("*W(/",    u"\u1F6F")
        t.add("*(/W",    u"\u1F6F")

        t.add("*)\\W",   u"\u1FAA")

        t.add("*A)=",    u"\u1F0E")
        t.add("*)=A",    u"\u1F0E")
        t.add("*A(=",    u"\u1F0F")
        t.add("*W)=",    u"\u1F6E")
        t.add("*)=W",    u"\u1F6E")
        t.add("*W(=",    u"\u1F6F")
        t.add("*(=W",    u"\u1F6F")

        t.add("A\\",    u"\u1F70")
        t.add("A/",     u"\u1F71")
        t.add("E\\",    u"\u1F72")
        t.add("E/",     u"\u1F73")
        t.add("H\\",    u"\u1F74")
        t.add("H/",     u"\u1F75")
        t.add("I\\",    u"\u1F76")
        t.add("I/",     u"\u1F77")
        t.add("O\\",    u"\u1F78")
        t.add("O/",     u"\u1F79")
        t.add("U\\",    u"\u1F7A")
        t.add("U/",     u"\u1F7B")
        t.add("W\\",    u"\u1F7C")
        t.add("W/",     u"\u1F7D")

        t.add("A)/|",   u"\u1F84")
        t.add("A(/|",   u"\u1F85")
        t.add("H)|",    u"\u1F90")
        t.add("H(|",    u"\u1F91")
        t.add("H)/|",   u"\u1F94")
        t.add("H)=|",   u"\u1F96")
        t.add("H(=|",   u"\u1F97")
        t.add("W)|",    u"\u1FA0")
        t.add("W(=|",   u"\u1FA7")

        t.add("A=",     u"\u1FB6")
        t.add("H=",     u"\u1FC6")
        t.add("I=",     u"\u1FD6")
        t.add("U=",     u"\u1FE6")
        t.add("W=",     u"\u1FF6")

        t.add("I\\+",   u"\u1FD2")
        t.add("I+\\",   u"\u1FD2")
        t.add("I/+",    u"\u1FD3")
        t.add("I+/",    u"\u1FD3")
        t.add("U\\+",   u"\u1FE2")
        t.add("U/+",    u"\u1FE3")

        t.add("U+\\",   u"\u1FE2")
        t.add("U+/",    u"\u1FE3")

        t.add("A|",     u"\u1FB3")
        t.add("A/|",    u"\u1FB4")
        t.add("H|",     u"\u1FC3")
        t.add("H/|",    u"\u1FC4")
        t.add("W|",     u"\u1FF3")
        t.add("W|/",    u"\u1FF4")
        t.add("W/|",    u"\u1FF4")

        t.add("A=|",    u"\u1FB7")
        t.add("H=|",    u"\u1FC7")
        t.add("W=|",    u"\u1FF7")

        t.add("R(",     u"\u1FE5")
        t.add("*R(",    u"\u1FEC")
        t.add("*(R",    u"\u1FEC")

        t.add("0", u"0")
        t.add("1", u"1")
        t.add("2", u"2")
        t.add("3", u"3")
        t.add("4", u"4")
        t.add("5", u"5")
        t.add("6", u"6")
        t.add("7", u"7")
        t.add("8", u"8")
        t.add("9", u"9")
        
        t.add("@", u"@")
        t.add("$", u"$")
        
        t.add(" ", u" ")
        
        t.add(".", u".")
        t.add(",", u",")
        t.add("'", u"'")
        t.add(":", u":")
        t.add(";", u";")
        t.add("_", u"_")

        t.add("[", u"[")
        t.add("]", u"]")
        
        t.add("\n", u"")
        
        
        return t

def main():

    book = Scrub()

if __name__ == "__main__":
    main()
