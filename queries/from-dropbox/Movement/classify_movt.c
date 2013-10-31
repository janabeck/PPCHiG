node: $ROOT

define: pos_tags.def

//print_indices: t

//(1)mov't:(2)left-mov't:(3)right-mov't

coding_query:

1: { t: (\*ICH\** Exists)
     f: ELSE
   }

2: { //leftward phrasal mov't
     P: ([1]phrase iDoms \*ICH\**) AND ([2]phrase Precedes [1]phrase) AND (\*ICH\** SameIndex [2]phrase)
     //leftward word mov't
     W:	([1]pos iDoms \*ICH\**) AND ([2]pos Precedes [1]pos) AND (\*ICH\** SameIndex [2]pos)
     //leftward ambiguous word/phrase mov't
     Y: (*Y iDoms \*ICH\**) AND (*Y-* Precedes *Y) AND (\*ICH\** SameIndex *Y-*)
     f: ELSE
   }

3: { //rightward extraposition appositives
     A: (.*-PRN* iDoms \*ICH\**) AND (.*-PRN* Precedes phrase) AND (\*ICH\** SameIndex phrase)
     //rightward extraposition CONJP, PP, CP-REL, RRC, CP-CMP, CP-DEG, CP-QUE
     E: ([1]CONJP*|PP*|CP-REL*|RRC*|CP-CMP*|CP-DEG*|CP-QUE* iDoms \*ICH\**) AND ([1]CONJP*|PP*|CP-REL*|RRC*|CP-CMP*|CP-DEG*|CP-QUE* Precedes [2]CONJP*|PP*|CP-REL*|RRC*|CP-CMP*|CP-DEG*|CP-QUE*) AND (\*ICH\** SameIndex [2]CONJP*|PP*|CP-REL*|RRC*|CP-CMP*|CP-DEG*|CP-QUE*)
     //rightward wh- mov't
     Q: ([1].* iDoms \*ICH\**) AND (W* iDoms [1].*) AND ([1].* Precedes [2].*) AND (\*ICH\** SameIndex [2].*)
     //rightward mov't from moved constituent
     S: ([1].* iDoms \*ICH\**) AND (.*-[0123456789] iDoms [1].*) AND ([1].* Precedes [2].*) AND (\*ICH\** SameIndex [2].*)
     //rightward phrasal mov't
     P: ([1]phrase iDoms \*ICH\**) AND ([1]phrase Precedes [2]phrase) AND (\*ICH\** SameIndex [2]phrase)
     //rightward word mov't
     W: ([1]pos iDoms \*ICH\**) AND ([1]pos Precedes [2]pos) AND (\*ICH\** SameIndex [2]pos)
     //rightward ambiguous word/phrase mov't
     Y: (*Y iDoms \*ICH\**) AND (*Y Precedes *Y-*) AND (\*ICH\** SameIndex *Y-*)
     f: ELSE
   }
