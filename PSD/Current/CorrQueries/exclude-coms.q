node: $ROOT

copy_corpus: t

query: ({1}VB.P*|VPRP* hasSister CP-COM*|IP-INF-COM*|CP-THT*|IP-INF-THT*|IP-SMC*|IP-PPL-THT*) AND ({2}FLAG iPrecedes VB.P*|VPRP*)

append_label{1}: -TRNS2

delete_leaf{2}:

