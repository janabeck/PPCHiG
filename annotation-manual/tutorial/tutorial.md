# Introduction

This guide offers a brief introduction to two things:

  #. the Penn Treebank style of syntactic annotation, as implemented for Ancient Greek

  #. the CorpusSearch 2 query langauge for searching and modifying Penn Treebank-style corpora

## Penn-Treebank format

The simple sentence 'I saw the man' is represented in Penn Treebank-style annotation as follows:

```
(IP-MAT (NP-SBJ (PRO I))  
        (VBD saw)  
        (NP-OB1 (D the)  
                (N man)))  
```

where...

  #. a pair of parentheses `( )` delineates each level

  #. each level contains two components:

    #. a label on the left (e.g., a phrase label, a part-of-speech (POS) label, etc.)

    #. content on the right (e.g., phrase(s), word(s), etc.)

## Basic POS tags

The full list of POS tags used in the Penn Parsed Corpus of Historical Greek (PPCHiG) can be found [here](http://www.ling.upenn.edu/~janabeck/PPCHiG_Annotation_Manual.xhtml#d0e116). In most categories, POS tags consist of a single string of letters, but in some categories (e.g., verbs), the core tags are 'extended' with 'dash' tags separated from the core tag by a hyphen `-`. Some examples of the most common and basic POS tags are as follows:

Tag               Meaning
-----             -----
N                 common noun, nominative singular
NS                common noun, nominative plural
ND                common noun, dative singular
NPR               proper noun, nominative singular
VBP-IMPF          verb, present imperfective
VBD-AOR-PASS      verb, aorist passive
VBNP-PRF          verb, perfect middle/passive infinitive
C                 complementizer (e.g., ὅτι 'that')
P                 preposition
D                 article, nominative singular (i.e., ὁ/ἡ/τό)
CLPRT             second-position particle (e.g., δέ, γάρ, περ, etc.)

Table:  POS tag examples

## Representing Discontinuities

Discontinuities are represented by means of placeholders—traces—in the structure that:

  #. show the origin of the displaced element

  #. indicate the connection between the displaced element and the trace by numerical co-indexation

### Example: `*T*` Traces for 'wh-' Movement

```
(CP-QUE (WNP-1 (WPRO What))          << displaced element
               (C 0)
        (IP-SUB (NP-OB1 *T*-1)       << co-indexed trace
                (VBD did)               indicating functional
                (NP-SBJ (PRO you))      position
                (VB see)))
```

