define: NoCase.def

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE

node: $ROOT

copy_corpus: t

query: ({1}article hasSister {2}VPA*|BPA*) AND (article iPrecedes VPA*|BPA*)

add_internal_node{1, 2}: NP-NEW