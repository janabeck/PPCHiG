node: $ROOT

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE

copy_corpus: t

query: ({1}P hasSister {2}NP*) AND
(P iPrecedes NP*)

add_internal_node{1, 2}: PP
replace_label{2}: NP