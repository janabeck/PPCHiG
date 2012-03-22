# This Python file uses the following encoding: utf-8

"""
ppchig_corpus_reader.py
Created 2012/3/22
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import corpus_reader

import os
import sys
import subprocess

def main():
	python_program = "python2"
	try:
	    with open("/dev/null","w") as sink:
	        subprocess.check_call(["which", python_program], stdout = sink)
	except subprocess.CalledProcessError:
	    python_program = "python"
	os.system(python_program + " " + "corpus_reader.py " + ' '.join(sys.argv[1:]))

if __name__ == "__main__":
	main()