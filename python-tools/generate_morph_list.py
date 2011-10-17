import re

def main():
    """Generate a list of all the morphological tags in an XML document."""
    
    in_name = raw_input("What is the name of your input XML file? ")
    print
    in_file = open(in_name, "rU")

    attr = raw_input("What is the name of the attribute that contains the morphological information? ")
    print

    pos = re.compile(attr + '=\"(.*?)\"')

    out_name = raw_input("What would you like the name of the output file to be? ")
    print
    out_file = open(out_name, "w")
    
    for line in in_file:
        list = pos.findall(line)
        for item in list:
            print >> out_file, item
    
if __name__ == "__main__":
    main()
