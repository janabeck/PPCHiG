define: Nominative.def

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE

node: $ROOT

copy_corpus: t

query: ({1}article hasSister {2}adjective) AND (article iPrecedes adjective)

add_internal_node{1, 2}: NP-ADJ
