define: Nominative.def

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE

node: $ROOT

copy_corpus: t

query: ([1]{1}adjective hasSister CONJ)
AND (CONJ hasSister [2]{2}adjective)
AND ([1]adjective iPrecedes CONJ)
AND (CONJ iPrecedes [2]adjective)

add_internal_node{1, 2}: ADJP
