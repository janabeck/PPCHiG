import re

# variables for split_words

exclude = re.compile("VB.*|VPR.*|BE.*|BPR.*")

non_words = re.compile("dash|{|\*|0|Herodotus|GreekNT|@")