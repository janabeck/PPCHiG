# This Python file uses the following encoding: utf-8

"""
corpus_reader.py
Created 2011/11/13
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import codecs
import sys
import re
from sets import Set

class Token:
    def __init__(self, parsed):
        """Initialize a token."""
        # id contains the token's ID as a string "Corpus,Book.x"
        self.id = ""

        # milestones contains all the milestones in a particular token
        self.milestones = []
        
        # words contains all the words in a sentence token, exclusive of punctuation, as a list
        self.words = []

        # text contains all the words in a sentence token, including punctuation, as a list
        self.text = []

        # labels contains all phrase, pos, and CODE, and ID labels in the tree
        self.labels = []
            
        # pos contains all the words in a sentence token with no punctuation or empty categories as a list of tuples
        # in which the first item is a Greek word and the second a POS tag
        self.pos = []

        # comments contains any comments in the token, as a list of strings
        self.comments = []

        # todos contains any TODOs in the token, as a list of strings
        self.todos = []

        # mans contains any MANs in the token, as a list of string
        self.mans = []

        # fulltree contains the whole tree as a dictionary with the key = index of the item, and the value = item
        self.tree = {}

        # root contains the top-most phrase structure label, e.g., IP-MAT
        self.root = ""
        
        # boolean indicating whether or not the sentence token has been parsed
        self.parsed = parsed

    def parse(self, sentence):
        # breaks string into components
        chunks = sentence.split()

        # loops through components of sentence token to add them to current instance of Token's attributes
        lastitem = ""
        countl = 0
        index = 0
        for item in chunks:
            # identifies labels
            if lastitem.strip() == "(" and item.strip() != "(":
                # identifies the root
                if countl == 2:
                    self.root = item
                    self.tree[index] = item
                else:
                    self.labels.append(item)
                    self.tree[index] = item
            elif item == "(" and lastitem == ")":
                item = "\n" + item
                self.tree[index] = item
            elif item == "(":
                self.tree[index] = item
                countl = countl + 1
            elif item == ")":
                    self.tree[index] = item
            # catches terminal nodes
            else:
                # catches IDs
                if lastitem == "ID":
                    self.id = item
                    self.tree[index] = item
                # catches empty categories
                elif "*" in item:
                    self.tree[index] = item
                # catches null pieces of split words
                elif item == "@":
                    self.tree[index] = item
                # catches null elements
                elif item == "0":
                    self.tree[index] = item
                # catches milestones
                elif "VS:" in item:
                    self.text.append(item)
                    self.milestones.append(item)
                    self.tree[index] = item
                # catches comments
                elif "COM:" in item:
                    self.tree[index] = item
                    self.comments.append(item)
                # catches TODOs
                elif "TODO:" in item:
                    self.tree[index] = item
                    self.todos.append(item)
                # catches MANs
                elif "MAN:" in item:
                    self.tree[index] = item
                    self.mans.append(item)
                # catches punctuation
                elif "." in item or "," in item or ";" in item or u"·" in item or "\"" in item:
                    if ("." in lastitem or "," in lastitem or ";" in lastitem or "\"" in lastitem):
                        self.text.append(item)
                        self.pos.append((item, lastitem))
                        self.tree[index] = item
                # catches everything else
                else:
                    if lastitem.strip() != "(":
                        if not "0" in item:
                            self.text.append(item)
                            self.pos.append((item, lastitem))
                            self.tree[index] = item
                            self.words.append(item)
            index += 1
            lastitem = item

class Parsed:
    def __init__(self):
        """Initialize a database of tokens."""
        # total number of tokens in file
        self.total = 0

        # dictionary with keys = ID #s and values as Token instances
        self.tokens = {}

        # list of all the Token instances in the database
        self.token_list = []
        
        # list of all the parsed Token instances in the database
        self.parsed_token_list = []

    def add(self, atoken):
        """Adds a Token instance to the database of tokens that Parsed is for."""
        
        self.token_list.append(atoken)
        if atoken.parsed:
            self.parsed_token_list.append(atoken)
        self.tokens[atoken.id] = atoken
        self.total += 1

    def print_text(self, id):
        """Prints only the text of a token."""

        token = self.tokens[id]
            
        for item in token.text:
            if not ":" in item:
                print item,

    def print_wmp(self, out_file, book):
        """Prints milestones, text, and punctuation in one-per-line format."""
            
        id_num = 1
            
        try:
            while id_num < self.total:
                sentence_id = "GreekNT," + book + "." + str(id_num)
                token = self.tokens[sentence_id]
                for item in token.text:
                    if "VS:" in item:
                        print >> out_file, "(CODE " + item + ")"
                    else:
                        print >> out_file, item
                id_num += 1
                      
            print "Printing to .wmp file completed."
            print
                
        except KeyError:
            sys.exit(0)

    def print_all_wmp(self, out_file):
        """Prints milestones, text, and punctuation in one-per-line format."""

        for token in self.token_list:
            for item in token.text:
                if "VS:" in item:
                    print >> out_file, "(CODE " + item + ")"
                else:
                    print >> out_file, item
                              
        print "Printing to .wmp file completed."
        print

    def print_all_words(self, out_file):
        """Prints all and only the words in one-per-line format."""

        for token in self.token_list:
            for item in token.words:
                print >> out_file, item

        print "Print to .wds file completed."
        print

    def print_tree(self, id):
        """Prints out a Token.fulltree as a string (for now!)."""

        token = self.tokens[id]

        for key in token.tree.keys():
            print token.tree[key],

    def add_milestones(self, out_file):
        """Adds continuity milestones."""

        lst_milestone = ""

        lst_letter = 0

        print_list = []

        for token in self.token_list:
            count = 0
            vs = token.tree[5]
            if not vs.startswith("{VS:"):
                print_list.append(token.tree[0] + " " + token.tree[1])
                count = 3
                max_count = len(token.tree.keys())
                if lst_letter == 0:
                    print_list.append(token.tree[2] + " (CODE " + lst_milestone[:(len(lst_milestone)-1)] + "a})\n")
                    lst_letter = 97
                else:
                    lst_letter += 1
                    print_list.append(token.tree[2] + " (CODE " + lst_milestone[:(len(lst_milestone)-1)] + chr(lst_letter) + "})\n")
                while count < max_count:
                    if token.tree[count].startswith("{VS:"):
                        lst_milestone = token.tree[count]
                        lst_letter = 0
                    if token.tree[count].find("(") != -1:
                        print_list.append(" (")
                    # catches labels
                    elif token.tree[count - 1].find("(") != -1 and token.tree[count + 1].find("(") == -1:
                        print_list.append(token.tree[count] + " ")
                    # catches terminal nodes
                    else:                              
                        print_list.append(token.tree[count])
                    count += 1
            else:
                for key in token.tree.keys():
                    if token.tree[key].startswith("{VS:"):
                        lst_milestone = token.tree[key]
                        lst_letter = 0
                    if token.tree[key].find("(") != -1:
                        print_list.append(" (")
                    # catches labels
                    elif token.tree[key - 1].find("(") != -1 and token.tree[key + 1].find("(") == -1:                  
                        print_list.append(token.tree[key] + " ")
                    # catches terminal nodes
                    else:
                        print_list.append(token.tree[key])

            print_list.append("\n\n")

        print "Printing to the output file..."
        print

        print >> out_file, "".join(print_list)

        print "Printing completed."
        print

    ## def print_lex(self, out_file):
    ##     """Prints lexicon-mode ready .pos file."""

    ##     id_num = 1
        
    ##     label = raw_input("What is the ID label?\n\
    ##     Use the format 'Corpus,Book.':")
    ##     print

    ##     while id_num <= self.total:
    ##         sentence_id = label + str(id_num)
    ##         token = self.tokens[sentence_id]
    ##         for word, postag in token.pos:
    ##             print >> out_file, word + "/" + postag

    ##         id_num += 1
                  
    ##     print "Printing to .lex file completed."
    ##     print

    def lemmas(self, out_file):
        """Prints all the unique lemmas in the file to the output file."""

        lemmas = Set([])

        for token in self.token_list:
            for tup in token.pos:
                try:
                    wl = tup[0].split("-")
                    lemma = wl[1]
                    lemmas.add(lemma)
                except IndexError:
                    pass

        lem_list = []

        for lemma in lemmas:
            lem_list.append(lemma)

        lem_list.sort()

        for lemma in lem_list:
            print >> out_file, lemma
            
    def pos_concordance(self):
        """Prints a concordance of words and POS tags in the corpus."""
            
        # dictionary keyed by pos tag with all the words the tag applies to as values
        concordance = {}

        lst = codecs.open("pos_list.txt", "w", "utf-8")

        pos_out = codecs.open("pos_concordance.txt", "w", "utf-8")
            
        for token in self.token_list:
            for tup in token.pos:
                try:
                    wl = tup[0].split("-")
                    word = wl[1]
                except IndexError:
                    word = tup[0]
                postag = tup[1]
                if postag in concordance:
                    concordance[postag].add(word)
                else:
                    concordance[postag] = Set([word])

        keys_list = []
                    
        for key in concordance:
            keys_list.append(key)

        keys_list.sort()
            
        for key in keys_list:
            print >> lst, key
            print >> pos_out, key + ": "
            for word in concordance[key]:
                print >> pos_out, word
            print >> pos_out
                
        print
        print "Printing completed."
        print
        
    def word_count(self):
        """Prints a word count of the *parsed* portion of the .psd file."""
        
        word_count = 0
        
        for token in self.parsed_token_list:
            for word in token.words:
                word_count += 1
                
        print "You have parsed " + str(word_count) + " words in this file."
        print
        
        print "You get a cookie!"
        print

    def swap(self, out_file, lemmatized):
        """Swaps words and POS tags with those in a word-by-word map file."""

        in_name = raw_input("What is the name of your POS map file?\nPlease include the file extension. ")

        map_file = codecs.open(in_name, "rU", "utf-8")

        new_tags = []

        for line in map_file:
            pair = line.split()
            word_lemma = pair[0]
            tag = pair[1]
            if not lemmatized:
                wl = word_lemma.split("-")
                word = wl[0]
                new_tags.append((word, word_lemma, tag))
            else:
                new_tags.append((word_lemma, word_lemma, tag))

        counter = 0

        last_tag = len(new_tags)

        print_list = []

        index = re.compile("[A-Z\-]+(\d)")

        for token in self.token_list:
            keys = token.tree.keys()
            for key in keys:
                if counter < last_tag - 1:
                    if token.tree[key] == new_tags[counter][0]:
                        token.tree[key] = new_tags[counter][1]
                        if new_tags[counter][2] == "NPRU":
                            if token.tree[key - 1] == "N":
                                token.tree[key - 1] = "NPR"
                            elif token.tree[key - 1] == "N$":
                                token.tree[key - 1] = "NPR$"
                            elif token.tree[key - 1] == "NA":
                                token.tree[key - 1] = "NPRA"
                            elif token.tree[key - 1] == "ND":
                                token.tree[key - 1] = "NPRD"
                            elif token.tree[key - 1] == "NS":
                                token.tree[key - 1] = "NPRS"
                            if token.tree[key - 1] == "NS$":
                                token.tree[key - 1] = "NPRS$"
                            if token.tree[key - 1] == "NSA":
                                token.tree[key - 1] = "NPRSA"
                            if token.tree[key - 1] == "NSD":
                                token.tree[key - 1] = "NPRSD"                                    
                        elif new_tags[counter][2] != "X":
                            if token.tree[key - 1].find("-PASS") != -1:
                                token.tree[key - 1] = new_tags[counter][2] + "-PASS"
                            elif re.match(index, token.tree[key - 1]):
                                num = re.match(index, token.tree[key - 1])
                                token.tree[key - 1] = new_tags[counter][2] + "-" + num.group(1)
                            else:
                                token.tree[key - 1] = new_tags[counter][2]
                        counter += 1

            for key in keys:
                if token.tree[key].find("(") != -1:
                    print_list.append(" (")
                elif token.tree[key - 1].find("(") != -1 and token.tree[key + 1].find("(") == -1:
                    print_list.append(token.tree[key] + " ")
                else:
                    print_list.append(token.tree[key])

            print_list.append("\n\n")

        print >> out_file, "".join(print_list)

    def correct_by_lemma(self, out_file):
        """Corrects POS by lemma, preserving properties such as case and number if needed."""

        in_name = raw_input("What is the name of your file containing lemmas to correct?\nPlease include the file extension. ")

        lem_file = codecs.open(in_name, "rU", "utf-8")

        lemmas = {}

        case = False

        number = False

        for line in lem_file:
            triple = line.split()
            lemmas[triple[0]] = triple[2]
            attrs = triple[1].split(",")
            if "case" in attrs:
                case = True
            if "number" in attrs:
                number = True

        print_list = []

        for token in self.token_list:
            keys = token.tree.keys()
            for key in keys:
                if "-" in token.tree[key] and token.tree[key + 1] == ")":
                    wl = token.tree[key].split("-")
                    lemma = wl[1]
                try:
                    if lemma in lemmas.keys():
                        if case and number:
                            # TODO
                            pass
                        elif case:
                            tag = token.tree[key - 1].rstrip()
                            if "$" in tag:
                                new_tag = lemmas[lemma] + "$"
                            elif tag.endswith("A"):
                                new_tag = lemmas[lemma] + "A"
                            elif tag.endswith("D"):
                                new_tag = lemmas[lemma] + "D"
                            elif tag.endswith("R"):
                                new_tag = tag
                            elif tag.endswith("S"):
                                new_tag = tag
                            else:
                                new_tag = lemmas[lemma]
                            token.tree[key - 1] = new_tag
                        else:
                            token.tree[key - 1] = lemmas[lemma]
                except UnboundLocalError:
                    pass
                lemma = ""

            for key in keys:
                if token.tree[key].find("(") != -1:
                    print_list.append(" (")
                elif token.tree[key - 1].find("(") != -1 and token.tree[key + 1].find("(") == -1:
                    print_list.append(token.tree[key] + " ")
                else:
                    print_list.append(token.tree[key])

            print_list.append("\n\n")

        print >> out_file, "".join(print_list)

    def mismatched(self, out_file):
        """Outputs the ID numbers of tokens with mismatched indices."""

        index1 = re.compile("[A-Z0-9$\+\-]+[\-=](\d)")

        index2 = re.compile(".*\*\-(\d)")

        labels = Set([])

        terms = Set([])

        for token in self.token_list:
            keys = token.tree.keys()
            for key in keys:
                if index1.match(token.tree[key]) and "{" not in token.tree[key]:
                    num = index1.match(token.tree[key])
                    if num.group(1) not in labels:
                        labels.add(num.group(1))
                    else:
                        terms.add(num.group(1))
                elif index2.match(token.tree[key]):
                    num = index2.match(token.tree[key])
                    terms.add(num.group(1))

            if len(labels) != len(terms):
                print token.id
                print labels
                print terms
                print
                print >> out_file, token.id

            labels.clear()

            terms.clear()
            

def main():
    try:
        # name of .psd file interested in reading
        filename = sys.argv[1]
    except IndexError:
        print "usage: corpus-reader.py .psd-file"
        sys.exit(1)

    corpus = read(filename)
      
    select(corpus)

def read(filename):
    print "Opening the .psd file..."
    print
      
    # opens .psd file for reading
    file = codecs.open(filename, "rU", "utf-8")
      
    # will contain text of a token
    sentence = ""
      
    # creates an instance of the class Parsed to hold all the tokens in the file
    aparsed = Parsed()
    
    # boolean variable for whether or not a sentence token has been parsed
    parsed = True

    print "Creating the database of tokens..."
    print
    # loops through file line by line to read tokens
    for line in file:
        # adds spaces around parentheses to make parsing easier
        line = line.replace("(", " ( ")
        line = line.replace(")", " ) ")
        if "<+ end-count +>" in line:
            parsed = False
        # starts collecting text of token
        elif "( ID" not in line:
            sentence = sentence + line.rstrip()
        # stops when finds an ID
        else:
            sentence = sentence + line.rstrip()
            # creates an instance of Token class
            atoken = Token(parsed)
            # parses current sentence token
            atoken.parse(sentence)
            aparsed.add(atoken)
            sentence = ""
                  
    print "Database completed."
    print
      
    return aparsed
      
def select(corpus):
    """Gives the user options of what to do now that the corpus has been read."""
    
    print "Select the option you wish to execute:"
    print "\ta. Print the text of a token."
    print "\tb. Print all the tokens in a sub-corpus of the .psd file in word, milestone, punctuation format."
    print "\tc. Print all the tokens in a .psd file in word, milestone, punctuation format."
    print "\td. Print the full tree of a token."
    print "\te. Print out the .psd file with additional continuity milestones."
    print "\tf. Print a list of all the unique lemmas in the file."
    ## print "\tf. Print out the whole corpus in lexicon-mode ready format."
    print "\tg. Print a concordance of POS tags and lemmas in the file."
    print "\th. Find the word count for the parsed portion of the .psd file."
    print "\ti. Print all and only the words in a .psd file. (For alignment with dependency corpora.)"
    print "\tj. Swap words and POS tags with words and POS tags from a word-by-word map file."
    print "\tk. Find trees with mismatched indices."
    print "\tl. Correct POS tags by lemma."
    choice = raw_input("Please type only the letter of your choice: ")
    print

    if choice == "a":
        token = raw_input("What is the ID # of the token in the format Corpus,Book.#? ")
        print
        corpus.print_text(token)
    elif choice == "b":
        book = raw_input("What is the name of the book you want to produce a .wmp file for? ")
        print
        out_name = book + ".wmp"
        out_file = codecs.open(out_name, "w", "utf-8")
        corpus.print_wmp(out_file, book)
    elif choice == "c":
        out_name = raw_input("What would you like the name of the output file to be?\nPlease do not include the file extension. ")
        print
        out_name = out_name + ".wmp"
        out_file = codecs.open(out_name, "w", "utf-8")
        corpus.print_all_wmp(out_file)
    elif choice == "d":
        token = raw_input("What is the ID # of the token in the format Corpus,Book.#? ")
        print
        corpus.print_tree(token)
    elif choice == "e":
        out_name = raw_input("What would you like the name of the output file to be?\nPlease do not include the file extension. ")
        print
        out_name = out_name + "-mm.psd"
        out_file = codecs.open(out_name, "w", "utf-8")
        corpus.add_milestones(out_file)
    elif choice == "f":
        out_name = raw_input("What would you like the name of the output file to be?\nPlease do not include the file extension. ")
        out_name = out_name + ".lem"
        out_file = codecs.open(out_name, "w", "utf-8")
        corpus.lemmas(out_file)
    ## elif choice == "f":
    ##     out_name = raw_input("What would you like the name of the output file to be?\nPlease do not include the file extension. ")
    ##     print
    ##     out_name = out_name + ".lex"
    ##     out_file = codecs.open(out_name, "w", "utf-8")
    ##     corpus.print_lex(out_file)
    elif choice == "g":
        corpus.pos_concordance()
    elif choice == "h":
        corpus.word_count()
    elif choice == "i":
        out_name = raw_input("What would you like the name of the output file to be?\nPlease do not include the file extension. ")
        print
        out_name = out_name + ".wds"
        out_file = codecs.open(out_name, "w", "utf-8")
        corpus.print_all_words(out_file)
    elif choice == "j":
        out_name = raw_input("What would you like the name of the output file to be?\nPlease do not include the file extension. ")
        print
        out_name = out_name + "-swap.psd"
        out_file = codecs.open(out_name, "w", "utf-8")
        lemmatized = False
        lem = raw_input("Is your current .psd file lemmatized? Please enter t or f. ")
        print
        if lem == "t":
            lemmatized = True
        corpus.swap(out_file, lemmatized)
    elif choice == "k":
        out_name = raw_input("What would you like the name of the output file to be?\nPlease do not include the file extension. ")
        print
        out_name = out_name + ".tokens"
        out_file = codecs.open(out_name, "w", "utf-8")
        print
        corpus.mismatched(out_file)
    elif choice == "l":
        out_name = raw_input("What would you like the name of the output file to be?\nPlease do not include the file extension. ")
        print
        out_name = out_name + ".new"
        out_file = codecs.open(out_name, "w", "utf-8")
        print
        corpus.correct_by_lemma(out_file)        

if __name__=="__main__":
    main()
