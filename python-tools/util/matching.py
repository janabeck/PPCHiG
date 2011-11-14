# This Python file uses the following encoding: utf-8

"""
matching.py
Created 2011/11/10
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

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
