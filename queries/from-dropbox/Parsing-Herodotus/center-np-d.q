define: Nominative.def

node: $ROOT

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE

copy_corpus: t

query: ({1}sa hasSister {2}[1]NP-NEW) AND
([1]NP-NEW hasSister {3}[2]NP-NEW) AND
(sa iPrecedes [1]NP-NEW) AND
([1]NP-NEW iPrecedes [2]NP-NEW) AND
([2]NP-NEW iDoms sn|adjective)

add_internal_node{1, 3}: NP-CEN
delete_node{3}:
