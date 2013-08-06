### README: corpus_reader.py

__NB:__ If file is in "dash" or "deep" format, it must have a `VERSION` tree at the top of the file:

```
( (VERISON (FORMAT dash)))
```
or
```
( (VERISON (FORMAT deep)))
```

All corpus output files are named with your original filename plus `.new`--e.g., `Test.psd.new`.

```
usage: corpus_reader.py [-h] [-s SETTINGS_PATH] [-c] [-i] [-m] [-p]
                        [-r OUTPUT_FILE] [-t] [-l]
                        psd [psd ...]
```

#### Help and settings

`-h` presents you with a help dialog for the program and its command-line arguments

`-s path-to-SETTINGS_FILE` loads your language-specific settings defined in a Python file

+ A sample settings file (for Greek) is as follows:

```
import re

# variables for split_words function

exclude = re.compile("VB.*|VPR.*|BE.*|BPR.*")

non_words = re.compile("dash|{|\*|0|Herodotus|GreekNT|@")
```

#### Description of the options:

`-c` to count words (exclusive of punctuation and empty categories)
   
+ punctuation is recognized by POS tag:

    - `,` `.` `'` `"` ` ` ` `LPAREN` `RPAREN`

    - If you have punctuation that is tagged otherwise, let me know so that I can potentially add it to the list of punctuation tags.

`-i` to renumber IDs

+ This function will also add IDs to tokens that don't have them.

+ If the first token in your corpus file (not including the VERSION cookie) doesn't have an ID, the program will prompt you for the name of your corpus and the name of the book in order to generate an ID in the format:
```
Corpus,Book:<milestones-separated-by-semicolons>.<#>
```

`-m` to add continuity milestones

+ This function will also reorder a collection of CODE nodes at the beginning of the token so that the milestone node always comes first.

+ This function always prints to output even if your corpus file is already in the proper format (potentially something I'll fix).

`-p` to print just the trees from a CS .out file (or a regular .psd file, but why would you want to do that?)

`-r path-to-OUTPUT-FILE` to replace tokens from an edited output file into the main corpus file

`-t` to generate a speed report (in words-per-hour) from Annotald's timelog.txt

`-l` to open a dialog on the command line that will help you split any words that have compound POS tags (separated by `-` or `+`)

+ If you have certain POS tags that contains `-` or `+` and are _always_ ineligible for splitting (e.g., words with dash tags to indicate case in some of the Penn-style corpora), you may name a variable `exclude` in a settings file that contains a regular expression for the tags to exclude.

+ You may also find it necessary to define (in the settings file) a variable `non_words` that contains a regular expression for non-words to exclude.

#### Less common functions

If you don't enter a command-line option, you will be presented with a menu of the less common functions and asked to input your choice.

a. Print a concordance of lemmas and POS tags in the corpus.

    + output is two files
    
        - `pos_list.txt`, which lists all the unique POS tags in your corpus (abstracting away from movement indices if present)
    
        - `pos_concordance.txt`, which lists (in an unsorted manner) all the lemmas that occur with each POS tag in the following format:
	  		       
			       TAG1:
			       lemma1 (frequency of lemma1)
			       lemma2 (freqency of lemma2)
			       etc.

			       TAG2:
			       lemma3 (frequency of lemma3)
			       etc.

b. Print a concordance of lemmas per category as defined in a input category definition file.
    
    + input (on the command line after your .psd file name) is a text file containing the following information on each line:

        - category-name: regular expression or list of POS tags separated by commas
        - for example:

			```
			noun: N, N$, NS, NS$
			proper-noun: NPR*
			```

    + output is the file `category-concordance.txt`, in the following format:

			 category-name:
			 lemma1 (frequency of lemma1)
			 etc.

c. Print all the unique lemmas (and their frequences) in a corpus file.

    + output file is `unique-lemmas.txt` in the following format:

			lemma1: frequency-of-lemma-1
			etc.

    + option to sort by frequency or alphabetically
    
d. Print a concordance of the word forms (and their frequencies) for the given lemma.

    + give the lemma you're interested in on the command line after the name of your .psd file

    + output is `<lemma>-concordance.txt` (where <lemma> is the lemma you entered) in the following format:

			word-form1: frequency-of-word-form1
			etc.

e. Print the text (words, punctuation) of the corpus file.

    + Extension is `.txt` instead of `.new`.

    + Prints words and punctuation one-per-line.

f. Print just the words of the corpus file.

    + Extension is `.txt` instead of `.new`.

    + Prints words one-per-line.

