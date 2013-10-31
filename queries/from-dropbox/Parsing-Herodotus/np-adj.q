define: Nominative.def

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE


node: $ROOT

copy_corpus: t

query: ({1}adjective hasSister {2}NP-NEW) AND
(NP-NEW iPrecedes adjective) AND
(NP-NEW iDoms !*PRO*) AND
(NP-NEW iDoms noun|adjective)

add_internal_node{1, 2}: NP-NEW
delete_node{2}:
