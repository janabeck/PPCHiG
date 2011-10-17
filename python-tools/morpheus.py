import codecs
import sys

from BeautifulSoup import BeautifulStoneSoup

class Morpheus():
    """A class that transforms Packard-style morphological tags into Penn-style POS tags."""

    def __init__(self):
        

def main():

    in_name = sys.argv[1]

    in_file = codecs.open(in_name, "rU", "utf-8")

    soup = BeautifulStoneSoup(in_file)

    words = soup.findAll('word')

    

if __name__ == "__main__":
    main()
