node: $ROOT

copy_corpus: t

query: ({1}VB.P*|VPRP* hasSister NP-OB1*|NP-OBQ*|NP-OBP*) AND ({2}FLAG iPrecedes VB.P*|VPRP*)

append_label{1}: -TRNS1

delete_leaf{2}: