import argparse
from bs4 import BeautifulSoup as BeautifulSoup

class PerseusDep():

    def __init__(self, file_base, n):

        self.soup = BeautifulSoup(open("xml/" + file_base + str(n) + ".xml", 'rU'), 'xml')

        self.out = open("xml/" + file_base + str(n) + "i.xml", 'w')

    def rename_COORD(self):
        """Rename COORD nodes to represent the relations they dominate."""

        coords = self.soup.find_all(relation='COORD')

        for coord in coords:
            sentence = self.soup.find(id=coord.parent['id'])
            words = sentence.find_all('word')
            for w in words:
                if w['head'] == coord['id']:
                    if w['relation'].find('SBJ_CO') != -1:
                        coord['relation'] = 'SBJ'

    def xml_print(self):

        print >> self.out, self.soup.prettify()

def main():
    parser = argparse.ArgumentParser(description='Process the input files.')
    parser.add_argument('-f', '--file_base', action = 'store', dest = "file_base", help='base of file names')
    parser.add_argument('-x', '--xml_file', action = 'store', dest = "xml_name", help='XML file')
    args = parser.parse_args()

    if args.xml_name:
        tmp = args.xml_name.split("/")
        base = tmp[1].replace('.xml', '')
        p = PerseusDep(base, '')
        p.rename_COORD()
        p.xml_print()
    elif args.file_base:
        n = 1

        while n < 2:
            p = PerseusDep(args.file_base, n)
            p.rename_COORD()
            p.xml_print()
            n += 1

    print '\a'

if __name__ == '__main__':
    main()