# Tutorial: Penn Treebank of Historical Greek

## Understanding the Annotation and Querying with CorpusSearch 2

### Jana E. Beck

#### University of Pennsylvania

# Introduction

This guide offers a brief introduction to two things:

  #. the Penn Treebank style of syntactic annotation, as implemented for Ancient Greek

  #. the CorpusSearch 2 query langauge for searching and modifying Penn Treebank-style corpora

## The Penn Historical Treebank philosophy

A primary motivating principle behind Penn Treebank-style annotation that is important to understand is that **the primary goal of the annotation is facilitation of automated search**, _not_ linguistically-accurate markup. To that end, the trees in Penn Treebank-style annotation are quite 'flat' compared to those found in many current theories (e.g., Minimalism) and are not binary-branching.

A corollary: Labels used in the annotation system should not be taken as descriptive claims about the language but as atheoretical tools to aid in the automatic classification of sentences according to various patterns and properties. There are known cases where a particular standard for annotation has been chosen even with full knowledge that it might or perhaps even probably is linguistically inaccurate. These cases are typically cases where simplicity of annotation and search has been prioritized at the expense of linguistic accuracy.

## Penn Treebank format

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

# POS Annotation

## Basic POS tags

The full list of POS tags used in the Penn Parsed Corpora of Historical Greek (PPCHiG) can be found [here](http://www.ling.upenn.edu/~janabeck/PPCHiG_Annotation_Manual.xhtml#d0e116). In most categories, POS tags consist of a single string of letters, but in some categories (e.g., verbs), the core tags are extended with 'dash' tags separated from the core tag by a hyphen `-`. Some examples of the most common and basic POS tags are as follows:

Tag         Meaning
------      -----
`D`         article (i.e., ὁ/ἡ/τό)
`N`         common noun
`NPR`       proper noun
`PRO`       pronoun
`WPRO`      relative or interrogative pronoun
`ADJ`       adjective
`ADV`       adverb
`P`         preposition
`C`         complementizer (e.g., ὅτι 'that')
`BE`...     non-participial forms of the verb εἰμί 'be'
`BPR`...    participial forms of the verb εἰμί 'be'
`VB`...     non-participial verb forms
`VPR`...    participial verb forms

## Unmarked morphological concepts

There are three morphological features that are _never_ marked in the PPCHiG:

+ gender
+ person
+ number on verbs

## Plurality

On nominals and _some_ related elements (determiners, etc.), plurality is represented by adding an `S` to the end of the POS tag.

Tag       Meaning
-----     -----
`DS`      article, plural (i.e., οἱ/αἱ/τά)
`NS`      common noun, plural
`NPRS`    proper noun, plural

Following the format established in the [Penn Parsed Corpora of Historical English (PPCHiE)](http://www.ling.upenn.edu/hist-corpora/annotation/index.html) any 'non-core' nominal and related elements _do not_ mark plurality. These include (but are not limited to):

+ adjectives
+ pronouns
+ participles

## Case

Case is represented on almost all types of words that have this property. Like plurality, case is represented by means of adding a letter to the end of a POS tag.

Suffix    Meaning
-----     -----
null      nominative
...`$`      genitive
...`A`      accusative
...`D`      dative

For example, `DSD` is a dative plural determiner (i.e., τοῖς/ταῖς). `ADJA` is an accusative adjective, _singular or plural_.

## Verbal POS tags

Penn Treebank-style annotation was originally designed for modern and historical English, a language that expresse the verbal concepts of tense, mood, and voice in an analytic fashion, via combinations of distinct verbs—that is, one or more auxiliary verbs together with a main verb in participial form.

+ simple past: I wrote.
+ present progressive: I am writing.
+ present perfect passive: It has been written.

In contrast to languages like English, Ancient Greek expresses these verbal concepts within one synthetic verbal form, the main verb of the sentence.

+ ἔγραψα 'I wrote'
+ γράφω 'I write/I am writing.'
+ γέγραπται 'It has been written.'

There are just 7 verbal POS tags in the PPCHiE.

Tag       Meaning
-----     -----
`VAG`     present participle
`VAN`     passive participle
`VB`      infinitive
`VBD`     past
`VBI`     imperative
`VBN`     perfect participle
`VBP`     present

Adopting the same strategy for Ancient Greek, using a single tag to represent each distinct tense, aspect, mood, voice, and finiteness combination, would require over 100 distinct tags. Alternatively, 'dash' tags separated from the main verbal tag by a hyphen can be used to add information about different verbal features without exploding the number of verbal tags. Using this strategy reduces the number of distinct verbal POS tags for Ancient Greek.

### Basic Verbal POS tags for Ancient Greek

Tag          Meaning
-----        -----
`VBP`...     primary sequence verb (includes present, future, and present perfect)
`VBD`...     secondary sequence verb (includes imperfect/past imperfective, aorist/past perfective, and pluperfect)
`VBN`...     infinitive
`VBI`...     imperative
`VBS`...     subjunctive
`VBO`...     optative
`VPR`...     participle

The pattern is the same for the copular verb εἰμί, which receives a special tag beginning in `BE`. For example, the core tag `BEO` appears on an optative form of εἰμί—e.g., εἴη.

### The ...`P` Suffix

Verbs that are morphologically middle, passive, or (morphologically speaking) ambiguously middle or passive, receive a `P` added to the core tag. For example, `VBNP` is the core tag that would appear on a middle or passive infinitive.

### Case on participles

Participial verbs (core tags `VPR` for verbs and `BPR` for εἰμί) take the same 'suffixes' as nominal elements (see [Case](#case) above) to indicate their case. The case suffixes appear _outside_ the `P` that may be present to mark middle or passive morphology. For example, `VPRP$` is a middle or passive participle in the genitive.

### Aspect, tense, etc.

The verbal concepts of aspect, tense, voice, and some functions of the optative are indicated with 'dash' tags.

Dash Tag         Meaning
-----            -----
`-AOR`           aorist (perfective aspect)
`-FUT`           future
`-IMPF`          imperfective aspect
`-IND`           marks optatives replacing indicatives in secondary sequence
`-KJV`           marks optatives replacing subjunctives in secondary sequence
`-PRF`           perfect aspect

Examples:

#.  ἴδμεν = `VBP-PRF`

#.  προβήσομαι = `VBPP-FUT-INTRNS` (see [next section](#marking-transitivity) for `-INTRNS`)

#.  ἀπῆλθε = `VBD-AOR`

#.  εἴη = `BEO-IMPF-KJV`
   
    ὅκως μὲν εἴη ἐν τῇ γῇ καρπὸς ἁδρός, τηνικαῦτα ἐσέβαλλε τὴν στρατιήν... (Hdt. 1.17.1, temporal clause equivalent of a protasis of a past general conditional)

    'When the crops in the land were ripe, he would invade...'

### Marking transitivity

Dash Tag         Meaning
-----            -----
`-INTRNS`        intransitive
`-PASS`          syntactic passive (not middle!)
`-TRNS1`         (direct) transitive
`-TRNS2`         (indirect) transitive

`P` marks verbal forms whose _morphology_ is non-active. In contrast, `-PASS` marks verbal forms in a clause where the _syntax_ involves the promotion of a typical object in an active construction to the subject of the sentence. 

Syntactic passives can have morphological forms that are either ambiguous between middle and passive voice or unambiguously passive, but the converse is not true: there are verb forms that are unambiguously passive with respect to their morphology but that have active (intransitive) syntax, not passive syntax.

#.  middle/passive morphology, active syntax = `VBPP-IMPF`(`-TRNS1`) 

    ...ἅμα δὲ κιθῶνι ἐκδυομένῳ συνεκδύεται καὶ τὴν αἰδῶ γυνή. (Hdt. 1.8.3)

    '...but at the same time as she removes her tunic, a woman dispenses with her modesty too.'

#.  middle/passive morphology, passive syntax = `VBPP-PRF-PASS`

    οὕτως γὰρ γέγραπται διὰ τοῦ προφήτου... (Matthew 2.5)

    'For thus it has been written through the prophet...'

#.  passive morphology, intransitive syntax: `VBDP-AOR-INTRNS`

    ...ἄγγελος Κυρίου κατ᾽ ὄναρ ἐφάνη αὐτῷ... (Matthew 1.20)
    
    '...an angel of the Lord appeared to him in a dream...'

`-INTRNS` marks verbs that have middle or passive morphology and exhibit intransitive syntax in the sentence. `-INTRNS` should be thought of as a set which includes `-PASS` as a subset: sometimes the decision between marking a verb as `-INTRNS` or `-PASS` is quite arbitrary. [This section in the PPCHiG annotation manual](http://www.ling.upenn.edu/~janabeck/PPCHiG_Annotation_Manual.xhtml#http://www.ling.upenn.edu/~janabeck/PPCHiG_Annotation_Manual.xhtml#VB_BE_notes) describes in more detail the various classes of verbs that typically get treated as passive or intransitive.

Finally, the `-TRNS1` and `-TRNS2` tags are automatically generated by query in the course of annotation in order to help make it easier to find verbs that need to be marked as `-PASS` or `-INTRNS`. For more information on the situations in which these tags are applied, see [here](http://www.ling.upenn.edu/~janabeck/PPCHiG_Annotation_Manual.xhtml#ext_verb_tags).

# Syntactic annotation

## Basic phrases and function tags

An extended list of common phrase + function tag combinations can be found [here](http://www.ling.upenn.edu/~janabeck/PPCHiG_Annotation_Manual.xhtml#d0e932). Phrase labels in most cases consist of the core tag for a particular category with an added `P` for 'phrase.' Phrase labels are extended with one or more 'dash' tags separated from the phrase label by a hyphen to indicate their function in the sentence.

Label       Meaning
-----       -----
`NP`        noun phrase
`ADJP`      adjective phrase
`PP`        prepositional phrase
`IP`        inflectional phrase (clause)
`CP`        complementizer phrase

Tag       Meaning
-----     -----
`-SBJ`    subject
`-OB1`    direct object
`-OB2`    indirect object
`-ATR`    attributive (includes possessive)
`-COM`    complement
`-PRD`    predicate
`-MAT`    matrix (clause)
`-SUB`    subordinate (clause)

Many function tags can appear on more than one type of phrase. For example, noun phrases can be subjects (`NP-SBJ`), but so can clauses (`CP-THT-SBJ`). Noun phrases can be complements (`NP-COM`, with adjectives such as ἄξιος), but so can infinitival clauses (`IP-INF-COM`, selected for by verb such as ἐθέλω), and participial phrases (`IP-PPL-COM`, in the case of supplementary participles to verbs such as τυγχάνω).

Extended tags on IPs and CPs tend to be more particular to those categories alone, since these tags often identify the type of clause. The most common types are:

Label       Meaning
-----       -----
`IP-MAT`    matrix (main) clause
`IP-SUB`    subordinate clause
`IP-INF`    infinitival clause
`IP-PPL`    participial clause
`CP-THT`    complement clause, indicative (where `THT` is mnemonic for English 'that')
`CP-COM`    complement clause, non-indicative
`CP-QUE`    direct or indirect question
`CP-REL`    relative clause
`CP-ADV`    adverbial clause

## Representing Discontinuities

Discontinuities are represented by means of placeholders—traces—in the structure that:

  #. show the origin of the displaced element

  #. indicate the connection between the displaced element and the trace by numerical co-indexation

#### Example: `*T*` Traces for 'wh-' Movement

```
(CP-QUE (WNP-1 (WPRO What))          << displaced element
               (C 0)
        (IP-SUB (NP-OB1 *T*-1)       << co-indexed trace
                (VBD did)               indicating functional
                (NP-SBJ (PRO you))      position
                (VB see)))
```

Different types of traces indicate different types of movement.

Trace     Meaning
-----     -----
`*`       A-movement[^#]
`*T*`     'wh-' movement
`*ICH*`   other A'-movement (`ICH` mnemonic for `I`nterpret `C`onstituent `H`ere)
`*CL*`    clitic displacement (clitic pronouns and verbs only)

[^#]: Rare—only A-movement in a passive is marked, and only in certain situations, see [here in the PPCHiG annotation manual](file:///Users/janabeck/Git/PPCHiG/annotation-manual/PPCHiG%20Annotation%20Manual.xhtml#a_movement).

# Search Queries with CorpusSearch 2

>" A corpus without a search program is like the Internet without a search engine."
>
> > Beth Randall

## CorpusSearch 2 on the Desktop

The software program CorpusSearch 2 (CS2) is used to query the Penn Historical Treebanks. This software is available for free download [here](http://sourceforge.net/projects/corpussearch/) for any operating system (Windows, Mac, Linux) and [the manual is also available on the web](http://corpussearch.sourceforge.net/CS-manual/Contents.html).

The interface to CS2 is on the command line.

### Running CS2 on Windows

On Windows, you can access the command line via Start > Run... and then typing `cmd` into the Run... dialog box.

The command to run CS2 on Windows is:

```
java -classpath "C:\<path-on-your-computer>\CS_2.003.jar" csearch/CorpusSearch <path-to-query>\<query>.q <path-to-corpus-file>\<parsed-file>.psd
```

**NB:** In the above command, anything between `<` and `>` will be particular either to your computer/filesystem or to the query you're running.

### Running CS2 on a Macintosh

On a Mac, you access the command line via the Terminal app from the Utilities folder (Appications/Utilities/) that comes pre-installed with OS X.

The command to run CS2 on a Mac is:

```
java -classpath /Users/<you>/<path-on-your-computer>/CS_2.003.jar csearch/CorpusSearch <path-to-query>/<query>.q <path-to-query>/<parsed-file>.psd 
```

**NB:** In the above command, anything between `<` and `>` will be particular either to your computer/filesystem or to the query you're running.


## Demo Web Interface

There is also a demo web interface for the book of Mark from the Greek New Testament [here](http://csearch2.ling.upenn.edu/GREEK/queryparsed.shtml). This demo allows you to query the book of Mark using a web implementation of the most basic functions of CorpusSearch 2.

**NB:** The web interface does *not* yet allow for search using Unicode Greek characters, so searches on the web interface are limited to searches for phrase and POS labels.

## Fundamentals of CorpusSearch 2

Two fundamental components are necessary to conduct a query with CS2, whether in the web interface or via a desktop installation.

#. a search domain, specified with `node: <domain>` at the top of the file
#. the query, specified after `query:` in the file

### The search domain

The search domain tells CS2 where to look for matches. For example, if you want to limit your search to match only within noun phrases (`NP`s), the top line of your CS2 query file will read:

```
node: NP*
```

Here the `*` is a wildcard that allows for _zero or more_ characters to follow the characters you have specified (in this case, `NP`)[^@].

[^@]: The use of `*` in this way reflects generalized, although limited, support for regular expressions in CS2. More information about CS2's support for regular expessions [is found here](http://corpussearch.sourceforge.net/CS-manual/QueryLanguage.html#regexp).

In other words, all of the following (among many other possibilities) would be possible domains in which CS2 would search for matches:

+ NP-SBJ
+ NP-COM
+ NP-2
+ NPR

In order to specify that CS2 search _anywhere_ in each tree token for matches, you must use a special variable since different tokens can have different categories at the top level (e.g., `IP-MAT` or `CP-QUE`). The special variable to search anywhere within each tree token is `$ROOT`. Many CS2 queries will thus begin with the line:

```
node: $ROOT
```

### The query

A full list of the search functions that CS2 contains can be found in the manual [here](http://corpussearch.sourceforge.net/CS-manual/SearchFunctions.html). Most of the CS2 search functions are binary, taking two arguments. The syntax of a query with a binary search function is `(<first-argument> searchFunction <second-argument>)`, where `<first-argument>` and `<second-argument>` are most commonly phrase and POS labels or lists thereof.

The most important functions are two sets of functions that query for dominance relations and precedence relations.

#### Dominance

There are two basic search functions for dominance: `Doms` and `iDoms` (see the CS2 manual for alternate possible spellings).

##### `Doms`

`Doms` queries for dominance at any level. In the query `(x Doms y)`, any `y` will match the query if `y` is contained within the subtree dominated by `x`.

For example, in the first sentence of Matthew in the Greek New Testament, if `x` is `NP-SBJ` and `y` is `N*` (which means anything that starts with N and contains zero or more characters following the initial `N`), any POS label or phrase label in the tree could be a match for the query.

```
( (FRAG (CODE {VS:1_1})
        (NP-SBJ (N ΒΙΒΛΟΣ-βίβλος)
                (NP-ATR (N$ γενέσεως-γένεσις)
                        (NP-ATR (NPR$ Ἰησοῦ-Ἰησοῦς)
                                (NP-PRN (NP (NPR$ Χριστοῦ-Χριστός))
                                            (CONJP (NP (N$ υἱοῦ-υἱός)
                                                       (NP-ATR (NPR$ Δαυεὶδ-Δαυίδ)
                                                               (NP-PRN (N$ υἱοῦ-υἱός)
                                                                       (NP-ATR (NPR$ Ἀβρααμ-Ἀβραάμ))))))))))
  (. .))
  (ID GreekNT,Matthew:1_1.1))
```

The query described above would be the following:

```
node: $ROOT

query: (NP-SBJ Doms N*)
```

And the output would be:

```
/*
PREFACE:  
Copyright 2010 Beth Randall
Date:  Thu Mar 08 02:29:58 EST 2012

command file:     Doms-example.q
output file:      Doms-example.out

node:   $ROOT
query:  (NP-SBJ Doms  N*) 
*/
/*
HEADER:
source file:  Test.psd
*/

/~*
ΒΙΒΛΟΣ-βίβλος γενέσεως-γένεσις Ἰησοῦ-Ἰησοῦς Χριστοῦ-Χριστός υἱοῦ-υἱός
Δαυεὶδ-Δαυίδ υἱοῦ-υἱός Ἀβρααμ-Ἀβραάμ.
(GreekNT,Matthew:1_1.1)
*~/
/*
1 FRAG:  4 NP-SBJ, 5 N
1 FRAG:  4 NP-SBJ, 7 NP-ATR
1 FRAG:  4 NP-SBJ, 8 N$
1 FRAG:  4 NP-SBJ, 10 NP-ATR
1 FRAG:  4 NP-SBJ, 11 NPR$
1 FRAG:  4 NP-SBJ, 13 NP-PRN
1 FRAG:  4 NP-SBJ, 14 NP
1 FRAG:  4 NP-SBJ, 15 NPR$
1 FRAG:  4 NP-SBJ, 18 NP
1 FRAG:  4 NP-SBJ, 19 N$
1 FRAG:  4 NP-SBJ, 21 NP-ATR
1 FRAG:  4 NP-SBJ, 22 NPR$
1 FRAG:  4 NP-SBJ, 24 NP-PRN
1 FRAG:  4 NP-SBJ, 25 N$
1 FRAG:  4 NP-SBJ, 27 NP-ATR
1 FRAG:  4 NP-SBJ, 28 NPR$
*/
( (FRAG (CODE {VS:1_1})
        (NP-SBJ (N ΒΙΒΛΟΣ-βίβλος)
                (NP-ATR (N$ γενέσεως-γένεσις)
                        (NP-ATR (NPR$ Ἰησοῦ-Ἰησοῦς)
                                (NP-PRN (NP (NPR$ Χριστοῦ-Χριστός))
                                            (CONJP (NP (N$ υἱοῦ-υἱός)
                                                       (NP-ATR (NPR$ Δαυεὶδ-Δαυίδ)
                                                               (NP-PRN (N$ υἱοῦ-υἱός)
                                                                       (NP-ATR (NPR$ Ἀβρααμ-Ἀβραάμ))))))))))
  (. .))
  (ID GreekNT,Matthew:1_1.1))
/*
FOOTER
  source file, hits/tokens/total
  Test.psd		1/1/1
*/
/*
SUMMARY:  
source files, hits/tokens/total
  Test.psd		1/1/1
whole search, hits/tokens/total
			1/1/1
*/
```

Here `NP-SBJ` matched everything below it that started with an `N`, which in this case meant everything else in the tree. But note that the number of hits in this sentence is still just 1: that's because there's only one `NP-SBJ` in the sentence to match. There are many _possible_ matches in the sentence, but CS2 only counts one match per boundary node (specified in `node:`).

In other words, the query `(NP-SBJ Doms N*)` is asking a simple yes/no question of the sentence fed to it: does this sentence contain the pattern? In fact, the sentence contains the pattern over a dozen times, but that doesn't matter, the only answer CS2 cares about is _yes_ or _no_—1 or 0.

From this example, you might think that it isn't possible to get more than one hit per sentence token in CS2, but in fact it is. You can match a query multiple times in one tree token if you manipulate the search domain. So, modifying the previous example a bit so that we're searching within noun phrases (`NP*`) and looking for any noun phrase (`NP*`) that dominates any noun or noun phrase (`N*`)[^&], the query would look like this:

[^&]: The fact that `N*` will match both nouns and noun phrases can be problematic, so in many cases in order to force matching at the POS level only, a definition file is used to full specify all of the POS tags (without wildcards) that count as a certain category. See [here in the CS2 manual](http://corpussearch.sourceforge.net/CS-manual/Def.html) for further details.

```
node: NP*

query: (NP* Doms N*)
```

And the output would be as follows, with the expected explosion of possibilities now that there are 3 wildcards in the query:

```
/*
PREFACE:  
Copyright 2010 Beth Randall
Date:  Thu Mar 08 02:43:31 EST 2012

command file:     Doms-example.q
output file:      Doms-example.out

node:   NP*
query:  (NP* Doms  N*) 
*/
/*
HEADER:
source file:  Test.psd
*/

/~*
ΒΙΒΛΟΣ-βίβλος γενέσεως-γένεσις Ἰησοῦ-Ἰησοῦς Χριστοῦ-Χριστός υἱοῦ-υἱός
Δαυεὶδ-Δαυίδ υἱοῦ-υἱός Ἀβρααμ-Ἀβραάμ.
(GreekNT,Matthew:1_1.1)
*~/
/*
4 NP-SBJ:  4 NP-SBJ, 5 N
4 NP-SBJ:  4 NP-SBJ, 7 NP-ATR
7 NP-ATR:  7 NP-ATR, 8 N$
4 NP-SBJ:  4 NP-SBJ, 8 N$
7 NP-ATR:  7 NP-ATR, 10 NP-ATR
4 NP-SBJ:  4 NP-SBJ, 10 NP-ATR
10 NP-ATR:  10 NP-ATR, 11 NPR$
7 NP-ATR:  7 NP-ATR, 11 NPR$
4 NP-SBJ:  4 NP-SBJ, 11 NPR$
10 NP-ATR:  10 NP-ATR, 13 NP-PRN
7 NP-ATR:  7 NP-ATR, 13 NP-PRN
4 NP-SBJ:  4 NP-SBJ, 13 NP-PRN
13 NP-PRN:  13 NP-PRN, 14 NP
10 NP-ATR:  10 NP-ATR, 14 NP
7 NP-ATR:  7 NP-ATR, 14 NP
4 NP-SBJ:  4 NP-SBJ, 14 NP
14 NP:  14 NP, 15 NPR$
13 NP-PRN:  13 NP-PRN, 15 NPR$
10 NP-ATR:  10 NP-ATR, 15 NPR$
7 NP-ATR:  7 NP-ATR, 15 NPR$
4 NP-SBJ:  4 NP-SBJ, 15 NPR$
13 NP-PRN:  13 NP-PRN, 18 NP
10 NP-ATR:  10 NP-ATR, 18 NP
7 NP-ATR:  7 NP-ATR, 18 NP
4 NP-SBJ:  4 NP-SBJ, 18 NP
18 NP:  18 NP, 19 N$
13 NP-PRN:  13 NP-PRN, 19 N$
10 NP-ATR:  10 NP-ATR, 19 N$
7 NP-ATR:  7 NP-ATR, 19 N$
4 NP-SBJ:  4 NP-SBJ, 19 N$
18 NP:  18 NP, 21 NP-ATR
13 NP-PRN:  13 NP-PRN, 21 NP-ATR
10 NP-ATR:  10 NP-ATR, 21 NP-ATR
7 NP-ATR:  7 NP-ATR, 21 NP-ATR
4 NP-SBJ:  4 NP-SBJ, 21 NP-ATR
21 NP-ATR:  21 NP-ATR, 22 NPR$
18 NP:  18 NP, 22 NPR$
13 NP-PRN:  13 NP-PRN, 22 NPR$
10 NP-ATR:  10 NP-ATR, 22 NPR$
7 NP-ATR:  7 NP-ATR, 22 NPR$
4 NP-SBJ:  4 NP-SBJ, 22 NPR$
21 NP-ATR:  21 NP-ATR, 24 NP-PRN
18 NP:  18 NP, 24 NP-PRN
13 NP-PRN:  13 NP-PRN, 24 NP-PRN
10 NP-ATR:  10 NP-ATR, 24 NP-PRN
7 NP-ATR:  7 NP-ATR, 24 NP-PRN
4 NP-SBJ:  4 NP-SBJ, 24 NP-PRN
24 NP-PRN:  24 NP-PRN, 25 N$
21 NP-ATR:  21 NP-ATR, 25 N$
18 NP:  18 NP, 25 N$
13 NP-PRN:  13 NP-PRN, 25 N$
10 NP-ATR:  10 NP-ATR, 25 N$
7 NP-ATR:  7 NP-ATR, 25 N$
4 NP-SBJ:  4 NP-SBJ, 25 N$
24 NP-PRN:  24 NP-PRN, 27 NP-ATR
21 NP-ATR:  21 NP-ATR, 27 NP-ATR
18 NP:  18 NP, 27 NP-ATR
13 NP-PRN:  13 NP-PRN, 27 NP-ATR
10 NP-ATR:  10 NP-ATR, 27 NP-ATR
7 NP-ATR:  7 NP-ATR, 27 NP-ATR
4 NP-SBJ:  4 NP-SBJ, 27 NP-ATR
27 NP-ATR:  27 NP-ATR, 28 NPR$
24 NP-PRN:  24 NP-PRN, 28 NPR$
21 NP-ATR:  21 NP-ATR, 28 NPR$
18 NP:  18 NP, 28 NPR$
13 NP-PRN:  13 NP-PRN, 28 NPR$
10 NP-ATR:  10 NP-ATR, 28 NPR$
7 NP-ATR:  7 NP-ATR, 28 NPR$
4 NP-SBJ:  4 NP-SBJ, 28 NPR$
*/
( (FRAG (CODE {VS:1_1})
        (NP-SBJ (N ΒΙΒΛΟΣ-βίβλος)
                (NP-ATR (N$ γενέσεως-γένεσις)
                        (NP-ATR (NPR$ Ἰησοῦ-Ἰησοῦς)
                                (NP-PRN (NP (NPR$ Χριστοῦ-Χριστός))
                                            (CONJP (NP (N$ υἱοῦ-υἱός)
                                                       (NP-ATR (NPR$ Δαυεὶδ-Δαυίδ)
                                                               (NP-PRN (N$ υἱοῦ-υἱός)
                                                                       (NP-ATR (NPR$ Ἀβρααμ-Ἀβραάμ))))))))))
  (. .))
  (ID GreekNT,Matthew:1_1.1))
/*
FOOTER
  source file, hits/tokens/total
  Test.psd		9/1/1
*/
/*
SUMMARY:  
source files, hits/tokens/total
  Test.psd		9/1/1
whole search, hits/tokens/total
			9/1/1
*/
```

##### `iDoms`

`iDoms` is mnemonic for 'immediately dominates.' The `iDoms` function behaves exactly like the `Doms` function except that `y` only `iDoms` `x` if `x` is a daughter of `y`.

For example, consider the following query, which is trying to match a noun phrase subject with an appositive noun phrase that is its daughter. (`-PRN` is mnemonic for 'parenthetical'; the same function tag is used for parenthetical `IP`s as well as appositives within the NP domain.)

```
node: $ROOT

query: (NP-SBJ iDoms NP-PRN)
```

The result of this query is zero matches because the only daughter of `NP-SBJ` in the first sentece of Matthew is `NP-ATR`.

```
/*
PREFACE:  
Copyright 2010 Beth Randall
Date:  Thu Mar 08 02:50:06 EST 2012

command file:     Doms-example.q
output file:      Doms-example.out

node:   $ROOT
query:  (NP-SBJ iDoms  NP-PRN) 
*/
/*
HEADER:
source file:  Test.psd
*/
/*
FOOTER
  source file, hits/tokens/total
  Test.psd		0/0/1
*/
/*
SUMMARY:  
source files, hits/tokens/total
  Test.psd		0/0/1
whole search, hits/tokens/total
			0/0/1
*/
```

#### Precedence

Parallel to the search functions relating to dominance, there are two search functions for precedence: `Precedes` and `iPrecedes`.

##### `Precedes`

`Precedes` queries for precedence regardless of intervening words or phrases. In the query `(x Precedes y)`, a match will be produced whenever `x` comes earlier in the sentence token than `y`. Querying for `(CONJ Precedes N*)` at the `$ROOT` level will match the following token from Mark 1.13:

```
( (IP-MAT (CODE {VS:1_13b})
          (CONJ καὶ-καί)
          (NP-SBJ (DS οἱ-ὁ) (NS ἄγγελοι-ἄγγελος))
          (VBD-IMPF διηκόνουν-διακονέω)
          (NP-OBQ (PROD αὐτῷ-αὐτός))
          (. .))
  (ID GreekNT,Mark:1_13b.20))
```

```
/*
PREFACE:  
Copyright 2010 Beth Randall
Date:  Thu Mar 08 13:53:42 EST 2012

command file:     Precedes-example.q
input file:       Test.psd2
output file:      Precedes-example.out

node:   $ROOT
query:  (CONJ Precedes  N*) 
*/
/*
HEADER:
source file:  Test.psd2
*/

/~*
καὶ-καί οἱ-ὁ ἄγγελοι-ἄγγελος διηκόνουν-διακονέω αὐτῷ-αὐτός.
(GreekNT,Mark:1_13b.20)
*~/
/*
1 IP-MAT:  4 CONJ, 6 NP-SBJ
1 IP-MAT:  4 CONJ, 9 NS
1 IP-MAT:  4 CONJ, 13 NP-OBQ
*/
( (IP-MAT (CODE {VS:1_13b})
          (CONJ καὶ-καί)
          (NP-SBJ (DS οἱ-ὁ) (NS ἄγγελοι-ἄγγελος))
          (VBD-IMPF διηκόνουν-διακονέω)
          (NP-OBQ (PROD αὐτῷ-αὐτός))
          (. .))
  (ID GreekNT,Mark:1_13b.20))
/*
FOOTER
  source file, hits/tokens/total
  Test.psd2		1/1/1
*/
/*
SUMMARY:  
source files, hits/tokens/total
  Test.psd2		1/1/1
whole search, hits/tokens/total
			1/1/1
*/
```

As in the example with `iDoms` [above](#idoms), there are three ways in which this sentence token matches the query, but together they count as a single hit since the search domain is the token itself.

##### `iPrecedes`

`iPrecedes` queries for the immediate precedence of one item before another. Replacing `Precedes` with `iPrecedes` in the previous example and running it on the same sentence token, we still get one match, but now there is only one instance of the pattern that causes the search function to evaluate to true: `CONJ` coming immediately before `NP-SBJ`.

Note that querying for `(CONJ iPrecedes D*)` instead of `(CONJ iPrecedes N*)` will also match the token because phrase labels (in this case `NP-SBJ`) don't count as occupying a place in the linear ordering of elements in the sentence.

```
/*
PREFACE:  
Copyright 2010 Beth Randall
Date:  Thu Mar 08 14:11:23 EST 2012

command file:     Precedes-example.q
input file:       Test.psd2
output file:      Precedes-example.out

node:   $ROOT
query:  (CONJ iPrecedes  D*) 
*/
/*
HEADER:
source file:  Test.psd2
*/

/~*
καὶ-καί οἱ-ὁ ἄγγελοι-ἄγγελος διηκόνουν-διακονέω αὐτῷ-αὐτός.
(GreekNT,Mark:1_13b.20)
*~/
/*
1 IP-MAT:  4 CONJ, 7 DS
*/
( (IP-MAT (CODE {VS:1_13b})
          (CONJ καὶ-καί)
          (NP-SBJ (DS οἱ-ὁ) (NS ἄγγελοι-ἄγγελος))
          (VBD-IMPF διηκόνουν-διακονέω)
          (NP-OBQ (PROD αὐτῷ-αὐτός))
          (. .))
  (ID GreekNT,Mark:1_13b.20))
/*
FOOTER
  source file, hits/tokens/total
  Test.psd2		1/1/1
*/
/*
SUMMARY:  
source files, hits/tokens/total
  Test.psd2		1/1/1
whole search, hits/tokens/total
			1/1/1
*/
```

### Complex queries

#### Combining dominance and precedence searches

A large number of the most useful CS2 queries involve a combination of (`i`)`Doms` and (`i`)`Precedes` queries, with the queries joined by the operator `AND`. A query can be written to find instances in which a modifier element (e.g., `PP` or `NP-ATR`) is center-embedded between the article and the noun in a DP. Broken down into parts, the query will be:

-   `(NP-* iDoms D*) AND`...

    a noun phrase immediately dominates a determiner, and...

-   `(NP-* iDoms N*) AND`...

    the same noun phrase also immediately dominates a noun, and...

-    `(NP-* iDoms PP|NP-*) AND`...

    the same noun phrase also immediately dominates a PP or another NP, and...

-    `(D* iPrecedes PP|NP-*) AND`...

    the determiner immediately precedes the PP or additional NP, and...

-    `(PP|NP-* iPrecedes N*)`

    the PP or additional NP immediately precedes the noun.

Taken together[^%]:

```
node: $ROOT

query: (NP-* iDoms D*) AND 
       (NP-* iDoms N*) AND 
       (NP-* iDoms PP|NP-*) AND 
       (D* iPrecedes PP|NP-*) AND 
       (PP|NP-* iPrecedes N*)
```

[^%]: Inserting a linebreak after `AND` is not necessary but is perhaps more readable.

Applied to the book of Mark, this query yields tokens containing noun phrases with center-embedding...

-   of a PP:

    ```
    (NP-OB1 (DA τὴν-ὁ)
            (PP (P ἐξ-ἐκ)
                (NP (PRO$ αὐτοῦ-αὐτός)))
            (NA δύναμιν-δύναμις)
            (RRC (VPRA-AOR ἐξελθοῦσαν-ἐξέρχομαι))))
    ```

-   or an NP:

    ```
    (NP-OB1 (DA τὴν-ὁ)
            (NP-ATR (PRO$+SLF ἑαυτοῦ-ἑαυτοῦ))
            (NA ψυχὴν-ψυχή))
    ```

#### Example: finding instances of extraction out of DPs vs. resumption

##### Query: extraction_from_DP.q

```
node: $ROOT

query: (CP-* iDoms W*) AND
       (CP-* iDoms IP-SUB*) AND
       (IP-SUB* iDoms NP-*) AND
       (NP-* iDoms NP-*|PP*) AND
       (NP-*|PP* iDoms \**) AND
       (\** SameIndex W*)
```

##### Query: resumptive_DP.q

```
node: $ROOT

query: (CP-* iDoms W*) AND
       (CP-* iDoms IP-SUB*) AND
       (IP-SUB* iDoms NP-*) AND
       (NP-* iDoms NP-*|PP*) AND
       (NP-*|PP* SameIndex W*)
```

### Logical operators

#### The `!` operator

The only option[^$] for defining a pattern negatively in CS2 is by using the `!` operator. The `!` operator negates the argument or list of arguments that it precedes. For example, the query `(NP-SBJ iDoms !PRO)` will return as matches all cases of non-pronominal subject noun phrases.

[^$]: The operators `OR` and `NOT` remain very buggy and should not be used, as the CS2 website warns [here](http://corpussearch.sourceforge.net/CS-manual/LogOps.html#OR).

#### The `|` operator

The pipe `|` is used for 'or' at the level of arguments to a search function. The query `(NP-SBJ iDoms Q|ADJ)` will return as matches all cases of subject noun phrases that contain a quantifier or an adjective.

## Advanced CorpusSearch 2 functions

### Coding queries

See [this section](http://corpussearch.sourceforge.net/CS-manual/Coding.html) of the CS2 manual.

### Revision queries

See [this section](http://corpussearch.sourceforge.net/CS-manual/Revise.html) of the CS2 manual.