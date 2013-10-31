define: Nominative.def

node: $ROOT

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE

copy_corpus: t

query: ({1}pa hasSister {2}PP) AND
(PP hasSister {3}NP-NEW) AND
(pa iPrecedes PP) AND
(PP iPrecedes NP-NEW) AND
(NP-NEW iDoms pn|adjective)

add_internal_node{1, 3}: NP-CEN
delete_node{3}:
