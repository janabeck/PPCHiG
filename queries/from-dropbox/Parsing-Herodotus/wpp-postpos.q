node: $ROOT

copy_corpus: t

query: (IP-MAT iDoms {1}P) AND (P hasSister {2}WNP) AND (WNP iPrecedes P)

add_internal_node{1, 2}: WPP
