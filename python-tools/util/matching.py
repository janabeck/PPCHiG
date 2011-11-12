def main():

    psd = open("gospels-check.txt", "rU")

    database = open("gospels-map.txt", "rU")

    outfile = open("match.txt", "w")

    count = 1

    words = []

    for line in database:
        pair = line.split()
        wl = pair[0].split("-")
        word = wl[0]
        words.append(word)

    index = 0
        
    for line in psd:
    	if line.rstrip() != words[index]:
	   print >> outfile, line.rstrip() + ":" + words[index]
       	   print >> outfile, "no match on line number " + str(count) + "!"
       	   print >> outfile

        index = index + 1

        count = count + 1

if __name__=="__main__":
   main()
