node: $ROOT

copy_corpus: t

query: ({1}VB.P*|VPRP* iDoms *-γίνομαι|*-γίγνομαι|*-κατάκειμαι|*-ἔρχομαι|*-πορεύομαι|*-κεῖμαι|*-καθέζομαι|*-κάθημαι|*-ἀφικνέομαι) AND ({2}FLAG iPrecedes VB.P*|VPRP*)

append_label{1}: -INTRNS

delete_leaf{2}: