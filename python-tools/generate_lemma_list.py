import codecs

from sets import Set

from BeautifulSoup import BeautifulStoneSoup

def main():
    """Print a list of all the lemmas that have a certain proiel-pos tag in the database."""

    in_file = codecs.open("gnt-greeknt.xml", "rU", "utf-8")

    print "Parsing the input file with BeautifulStoneSoup..."
    print

    soup = BeautifulStoneSoup(in_file)

    print "Finding all the tokens..."
    print

    tokens = soup.findAll('token')

    tag_list = raw_input("What proiel-pos tags do you want to find all the lemmas for? Enter these as a comma-separated list. ")
    print

    tags = tag_list.split(",")

    out_file = codecs.open("GNT-lemma-list.txt", "w", "utf-8")
    
    for tag in tags:

        lemmas = Set([])
        
        for token in tokens:
            try:
                if token['morph-features'].find(tag) != -1:
                    features = token['morph-features'].split(",")
                    lemma = features[0]
                    lemmas.add(lemma)
            except KeyError:
                pass

        print >> out_file, "The lemmas for tag " + tag + " are: "
        print >> out_file

        for lemma in lemmas:
            print >> out_file, lemma
        
if __name__ == "__main__":
    main()
