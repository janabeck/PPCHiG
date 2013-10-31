define: Nominative.def

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE|VPA*

node: $ROOT

copy_corpus: t

query: ({1}pa hasSister {2}NP-NEW) AND
(pa iPrecedes NP-NEW) AND
(NP-NEW iDoms !*PRO*) AND
(NP-NEW iDoms pn|adjective)

add_internal_node{1, 2}: NP-NEW
delete_node{2}:
