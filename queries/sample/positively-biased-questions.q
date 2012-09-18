/* finds positively-biased questions (e.g., "Aren't you happy?") */

node: $ROOT

query: (CP-QUE* iDoms *PRTQ*) AND (*PRTQ* iDoms *οὐ*|*οὔ*|*μή*)