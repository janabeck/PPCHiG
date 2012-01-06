## Aaron sent this to me to model working with Corpus Search via Python

#!/usr/bin/python

# TODO: rerun whole changed column? (add aggressive switch to config?)
# add option to run new CS query, with appropriate file renames, or just print (dry-run)

import os, subprocess, sys, tempfile
from commands import mkarg

CS_COMMAND = "java -classpath /Users/aecay/Documents/CS_2.003.jar csearch/CorpusSearch"

def get_coding_from_file(file):
    out = subprocess.Popen("sed -n -e '/coding_query:/,/*\//p' <" + file,
                           shell = True, stdout=subprocess.PIPE).communicate()[0]
    out = out.split("\n")
    out.pop(0)
    out.pop()
    return "\n".join(out)

def print_usage():
    print "This is the Magic Frobnicator"
    print "Usage: " + sys.argv[0] + " <name of coding file> <name of output file>"

def main():
    if len(sys.argv) != 3:
        print_usage()
        exit(1)
    coding_file = sys.argv[1]
    output_file = sys.argv[2]
    prev_coding = get_coding_from_file(output_file)
    with open(coding_file) as f:
        coding_contents = f.read()
    temp_fd, temp_path = tempfile.mkstemp(".c", dir = ".")
    temp_fd2, temp_path2 = tempfile.mkstemp(".out", dir = ".")
    os.close(temp_fd2)
    os.write(temp_fd, coding_contents)
    os.close(temp_fd)
    ret = subprocess.call(CS_COMMAND + mkarg(temp_path) + mkarg(temp_path2) +
                          " &>/dev/null", shell = True)
    if ret != 0:
        print "CorpusSearch error!  Check your coding file."
        exit(2)
    new_coding = get_coding_from_file(temp_path+"od")

    os.unlink(temp_path)
    os.unlink(temp_path2)
    os.unlink(temp_path+"od")

    temp_fd3, temp_path3 = tempfile.mkstemp(dir = ".")
    temp_fd4, temp_path4 = tempfile.mkstemp(dir = ".")

    os.write(temp_fd3, prev_coding)
    os.close(temp_fd3)

    os.write(temp_fd4, new_coding)
    os.close(temp_fd4)

    diff = subprocess.Popen("diff -U 0 -F \"^[0-9]\\+:\" " + mkarg(temp_path3) +
                            mkarg (temp_path4) +
                            " | sed -e'/^+++/d' -e's/@@.*@@/}\\n/' -e'/^-/d' -e 's/^+//'",
                            shell = True, stdout = subprocess.PIPE).communicate()[0]
    diff = diff.split("\n")
    diff.pop(0)
    diff = "\n".join(diff) + "\n}"

    print diff

    os.unlink(temp_path3)
    os.unlink(temp_path4)
    
if __name__ == "__main__":
    main()


