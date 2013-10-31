node: $ROOT

copy_corpus: t

query: ([1]{1}NUM hasSister [2]{2}NUM)
AND ([1]NUM iPrecedes [2]NUM)

add_internal_node{1, 2}: NUMP
