// Copyright (c) 2011 Anton Karl Ingason, Aaron Ecay, Jana Beck

// This file is part of the Annotald program for annotating
// phrase-structure treebanks in the Penn Treebank style.

// This file is distributed under the terms of the GNU Lesser General
// Public License as published by the Free Software Foundation, either
// version 3 of the License, or (at your option) any later version.

// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
// General Public License for more details.

// You should have received a copy of the GNU Lesser General Public
// License along with this program.  If not, see
// <http://www.gnu.org/licenses/>.

/*
 *  Displays a context menu for setting case extensions according to
 *  the IcePaHC annotation scheme
 *  caseTags indicates which tags should be interpreted as case tags
 *  for this purpose
 */ 
var displayCaseMenu = false;
var caseTags=[];

/*
 * These two functions should return true if the string argument is a valid
 * label for a branching (-Phrase-) and non-branching (-Leaf-) label, and
 * false otherwise.
 */
var leaf_parser = new leaf_grammar_parser();
var phrase_parser = new phrase_grammar_parser();

function testValidPhraseLabel (str) {
   return phrase_parser.parse(str) instanceof waxeye.AST;
}

function testValidLeafLabel (str) {
   return leaf_parser.parse(str) instanceof waxeye.AST;
}

/* extensions are treated as not part of the label for various purposes, 
 * they are all binary, and they show up in the toggle extension menu  
 */
var extensions=["-SBJ","-LFD","-RSP","-PRN","-SPE","-CL","-ZZZ","-XXX","FLAG"]

/* clause extensions are treated as not part of the label for various purposes,
 * they are all binary, and they show up in the toggle extension menu
 */
var clause_extensions=["-IMP","-PRN","-SPE","-SBJ","-ZZZ","-XXX","FLAG"]

/* verbal extensions are treated as not part of the label for various purposes,
 * they are all binary, and they show up in the verbal extension menu (TODO)
 */
var vextensions=["-FUT","-IMPF","-AOR","-PRF","-TRNS1","-TRNS2","-INTRNS","-PASS","-IND","-KJV","-NOM","-GEN","-ACC","-DAT","-CL","FLAG"];

/*
 * Keycode is from onKeyDown event.
 * This can for example be tested here:
 * http://www.asquare.net/javascript/tests/KeyCode.html
 */
function customCommands(){
    // left hand commands
    addCommand({ keycode: 65 }, toggleVerbalExtension, "-AOR"); // a
    addCommand({ keycode: 65, shift: true}, nextAndValidate); // shift + a
    addCommand({ keycode: 65, ctrl: true }, toggleVerbalExtension, "-INTRNS"); // ctrl + a
    // adverb phrase shortcuts
    addCommand({ keycode: 66 }, setLabel, ["ADVP", "ADVP-DIR", "ADVP-LOC", "ADVP-TMP"]); // b
    // adverbial CPs
    addCommand({ keycode: 66, shift: true }, setLabel, ["CP-ADV","CP-PRP","CP-RES"]); // shift + b
    addCommand({ keycode: 66, ctrl: true }, addBkmk); // ctrl + b
    addCommand({ keycode: 67 }, coIndex); // c
    addCommand({ keycode: 67, shift: true}, addCom); // shift + c
    addCommand({ keycode: 67, ctrl: true }, toggleVerbalExtension, "-CL"); // ctrl + c
    addCommand({ keycode: 68 }, pruneNode); // d
    addCommand({ keycode: 68, shift: true}, setLabel, ["CLPRT","INTJ","INTJP","PRTQ","FW","AN","KE"]); // shift + d
    addCommand({ keycode: 68, ctrl: true}, setLabel, ["NEG"]); // ctrl + d
    // NP-within-NP shortcuts
    addCommand({ keycode: 69 }, setLabel, ["NP-ATR","NP-PRN","NP-PAR","NP-CMP","NP-COM"]); // e
    addCommand({ keycode: 69, shift: true }, setLabel, ["NP", "NY"]); // shift + e
    addCommand({ keycode: 69, ctrl: true }, fixError); // ctrl + e
    addCommand({ keycode: 70 }, setLabel, ["PP"]); // f
    addCommand({ keycode: 70, shift: true }, toggleVerbalExtension, "-FUT"); // shift + f
    addCommand({ keycode: 70, ctrl: true }, setLabel, ["FRAG"]); // ctrl + f
    // adjective phrase shortcuts
    addCommand({ keycode: 71 }, setLabel, ["ADJP","ADJP-PRD","ADJP-SPR","ADJX","ADJY"]); // g
    addCommand({ keycode: 71, shift: true }, setLabel, ["NP-AGT"]); // shift + g

    addCommand({ keycode: 81 }, setLabel, ["CONJP"]); // q
    addCommand({ keycode: 81, shift: true}, autoConjoin); // shift + q
    addCommand({ keycode: 81, ctrl: true}, setLabel, ["CP-QUE","QP","QTP","QX","QY"]); // ctrl + q
    
    // relative clauses and variations thereof
    addCommand({ keycode: 82 }, setLabel, ["CP-REL","RRC","CP-CMP","CP-FRL","CP-EOP","CP-EXL","CP-CAR"]); // r
    addCommand({ keycode: 82, shift: true }, setLabel, ["NP-FLAG","NP#"]); // shift + r
    addCommand({ keycode: 82, ctrl: true }, toggleExtension, "-RSP"); // ctrl + r
    // basic sentence-level elements
    addCommand({ keycode: 83 }, setLabel, ["IP-SUB","IP-MAT","IP-IMP"]); // s
    addCommand({ keycode: 83, shift: true}, setLabel, ["IP", "IY"]); // shift + s
    addCommand({ keycode: 83, ctrl: true}, toggleVerbalExtension, "-PASS"); // ctrl + s
    // complement CPs
    addCommand({ keycode: 84 }, setLabel, ["CP-THT","CP-COM","CP-DEG"]); // t
    addCommand({ keycode: 84, shift: true}, toggleVerbalExtension, "-TRNS1"); // shift + t
    addCommand({ keycode: 84, ctrl: true}, toggleVerbalExtension, "-TRNS2"); // ctrl + t

    // participial clauses
    addCommand({ keycode: 86 }, setLabel, ["IP-PPL","IP-ABS","IP-SMC","IP-PPL-COM","IP-PPL-THT"]); // v
    // infinitive clauses
    addCommand({ keycode: 86, shift: true }, setLabel, ["IP-INF","IP-INF-COM","IP-INF-PRP","IP-INF-SBJ","IP-INF-THT","IP-INF-ABS"]); // shift + v
    // argument NP shortcuts
    addCommand({ keycode: 87 }, setLabel, ["NP-SBJ","NP-OB1","NP-OB2","NP-OBP","NP-OBQ","NP-PRD"]); // w
    addCommand({ keycode: 87, shift: true }, setLabel, ["WADJP","WADVP","WNP","WPP","WQP"]); // shift + w

    addCommand({ keycode: 88 }, makeNode, "XP"); // x
    addCommand({ keycode: 88, shift: true }, setLabel, ["XP"]); // shift + x
    addCommand({ keycode: 88, ctrl: true}, toggleExtension, "-XXX"); // ctrl + x

    addCommand({ keycode: 90 }, undo); // z
    addCommand({ keycode: 90, shift: true }, splitWord); // shift + z

    // left hand number commands
    addCommand({ keycode: 49 }, leafBefore); // 1
    addCommand({ keycode: 50 }, leafAfter); // 2
    // non-argument NP shortcuts
    addCommand({ keycode: 51 }, setLabel, ["NX","NP-ADV","NP-AGT","NP-DIR","NP-INS","NP-LOC","NP-MSR","NP-SPR","NP-TMP","NP-VOC","NP-ADT"]); // 3
    addCommand({ keycode: 51, shift: true}, addTodo); // shift + 3
    addCommand({ keycode: 51, ctrl: true}, addMan); // ctrl + 3
    addCommand({ keycode: 52 }, toggleExtension, "-PRN"); // 4
    addCommand({ keycode: 53 }, toggleExtension, "-SPE"); // 5

    // right hand commands
    //addCommand({ keycode: 72 }, ); // h
    addCommand({ keycode: 73 }, toggleVerbalExtension, "-IMPF"); // i
    addCommand({ keycode: 73, shift: true }, toggleVerbalExtension, "-IND"); // shift + i
    addCommand({ keycode: 73, ctrl: true }, toggleExtension, "-IMP"); // ctrl + i
    //addCommand({ keycode: 74 }, ); // j
    addCommand({ keycode: 75 }, toggleVerbalExtension, "-KJV"); // k
    addCommand({ keycode: 76 }, editLemmaOrLabel); // l
    addCommand({ keycode: 76, shift: true }, displayRename); // shift + l
    addCommand({ keycode: 76, ctrl: true }, toggleExtension, "-LFD"); // ctrl + l
    //addCommand({ keycode: 77 }, ); // m
    //addCommand({ keycode: 78 }, ); // n
    //addCommand({ keycode: 79 }, ); // o
    addCommand({ keycode: 80 }, toggleVerbalExtension, "-PRF"); // p

    //addCommand({ keycode: 85 }, ); // u

    //addCommand({ keycode: 89 }, ); // y

    addCommand({ keycode: 32 }, clearSelection); // spacebar
    addCommand({ keycode: 192 }, toggleLemmata); // `

}


/*
 * Default label suggestions in context menu 
 */
var defaultConMenuGroup = ["VBP","VBPP","VBD","VBDP","VBN","VBNP","VBS","VBSP","VBO","VBOP","VBI","VBIP","VBDX","VBIX","VBNX","VBOX","VBPX","VBSX"];

/*
 * Phrase labels that are suggested in context menu when one of the other ones is set
 */
function customConMenuGroups(){
    addConMenuGroup( ["ADJ-NOM","ADJ-GEN","ADJ-ACC","ADJ-DAT","ADJR","ADJS"] );
    addConMenuGroup( ["ADJP","ADJP-PRD","ADJP-SPR","ADJX","ADJY"] );
    addConMenuGroup( ["ADV","ADVR","ADVS","NEG","P"] );
    addConMenuGroup( ["ADVP","ADVP-DIR","ADVP-LOC","ADVP-TMP","PP"] );
    addConMenuGroup( ["AN","KE"] );
    addConMenuGroup( [",","."] );
    addConMenuGroup( ["BED","BEI","BEN","BEO","BEP","BES","BPR"] );
    addConMenuGroup( ["CLGE","CLPRO-NOM","CLPRO-GEN","CLPRO-ACC","CLPRO-DAT","CLPRT","CLQ-NOM","CLQ-GEN","CLQ-ACC","CLQ-DAT","CLTE"] );
    addConMenuGroup( ["C","P","CONJ","ADV","WADV"] );
    addConMenuGroup( ["D-NOM","DS-NOM","DEM-NOM","DEMS-NOM","CLPRO-DAT","WPRO-NOM","WD-NOM","D-ACC","DS-ACC","DEM-ACC","DEMS-ACC","WPRO-ACC","WD-ACC"] );
    addConMenuGroup( ["D-GEN","DS-GEN","WPRO-GEN","WD-GEN"] );
    addConMenuGroup( ["D-DAT","DS-DAT","WPRO-DAT","WD-DAT"] );
    addConMenuGroup( ["INTJ","INTJP","FW","PRTQ"] );
    addConMenuGroup( ["Q-NOM","Q-GEN","Q-ACC","Q-DAT","QR","QS","QV"] );
    addConMenuGroup( ["N-NOM","N-GEN","N-ACC","N-DAT","NS-NOM","NS-GEN","NS-ACC","NS-DAT","NPR-NOM","NPR-GEN","NPR-ACC","NPR-DAT","NPRS-NOM","NPRS-GEN","NPRS-ACC","NPRS-DAT"] );
    addConMenuGroup( ["NX","NY","NP-ADT","NP-ADV","NP-AGT","NP-DIR","NP-INS","NP-LFD","NP-LOC","NP-MSR","NP-RSP","NP-SPR","NP-TMP","NP-VOC","QP"] );
    addConMenuGroup( ["NP-SBJ","NP-OB1","NP-OB2","NP-OBP","NP-OBQ","NP-PRD","NP-ATR","NP-PRN","NP-PAR","NP-CMP","NP-COM"] );
    addConMenuGroup( ["VPR-NOM","VPRP-NOM","VPR-GEN","VPRP-GEN","VPR-ACC","VPRP-ACC","VPR-DAT","VPRP-DAT"] );
    addConMenuGroup( ["WADJ-NOM","WADJ-GEN","WADJ-ACC","WADJ-DAT","WD-NOM","WD-GEN","WD-ACC","WD-DAT","WP","WQ"] );
    addConMenuGroup( ["WADJP","WADJX","WADVP","WADVX","WNP","WNX","WPP","WQP"] );
    addConMenuGroup( ["CP","CP-ADV","CP-CAR","CP-COM","CP-CMP","CP-DEG","CP-EOP","CP-EXL","CP-FRL","CP-PRP","CP-QUE","CP-REL","CP-RES","CP-THT"] );
    addConMenuGroup( ["IP","IY","RRC","IP-ABS","IP-IMP","IP-INF","IP-INF-COM","IP-INF-PRP","IP-INF-SBJ","IP-MAT","IP-PPL","IP-PPL-COM","IP-SMC","IP-SUB"] );
    addConMenuGroup( ["QP","QX","QY"] );
    addConMenuGroup( ["OTHER-NOM","OTHER-GEN","OTHER-ACC","OTHER-DAT"] );
    //addConMenuGroup( [] );
}

/*
 * Context menu items for "leaf before" shortcuts
 */
function customConLeafBefore(){
        addConLeafBefore( "NP-SBJ", "*con*");
        addConLeafBefore( "NP-SBJ", "*pro*");
        addConLeafBefore( "NP-SBJ", "*mat*");
        addConLeafBefore( "NP-SBJ", "*exp*");
        addConLeafBefore( "NP-SBJ", "*");
        addConLeafBefore( "BEP-IMPF", "*");
        addConLeafBefore( "BED-IMPF", "*");
        addConLeafBefore( "WADVP", "0");
        addConLeafBefore( "WNP", "0");
        addConLeafBefore( "WADJP", "0");
        addConLeafBefore( "C", "0");       
}

// My functions

function addCom() {
    makeLeaf(true, "CODE", "{COM:}");
}

function addTodo() {
    makeLeaf(true, "CODE", "{TODO:}");
}

function addMan() {
    makeLeaf(true, "CODE", "{MAN:}");
}

function addBkmk() {
    makeLeaf(true, "CODE", "{BKMK}");
}

// Aaron's magical autoConjoin

function autoConjoin() {
    if (!startnode || endnode) return;
    var savestartnode = startnode;
    var selnode = $(startnode);
    var label = getLabel(selnode);
    var conjnode = selnode.children(".CONJ").first();
    if (conjnode) {
        startnode = selnode.children().first().get(0);
        endnode = conjnode.prev().get(0);
        makeNode(label);
        startnode = conjnode.get(0);
        endnode = selnode.children().last().get(0);
        makeNode("CONJP");
        var conjpnode = $(startnode);
        startnode = conjpnode.children().get(1);
        endnode = conjpnode.children().last().get(0);
        makeNode(label);
        startnode = savestartnode;
        endnode = undefined;
        updateSelection();
    }
}

function nextAndValidate() {
   var tmp, tmp2;
   do {
       tmp2 = currentText($("#editpane"));
       advanceTree("/nextTree", undefined, false);
       validateTreesSync(false);
       tmp = $("#editpane").html();
   }
   while (!/-FLAG/.test(tmp) && tmp2 != currentText($("#editpane")))
}

// An example of a CSS rule for coloring a POS tag.  The styleTag
// function takes care of setting up a (somewhat complex) CSS rule that
// applies the given style to any node that has the given label.  Dash tags
// are accounted for, i.e. NP also matches NP-FOO (but not NPR).  The
// lower-level addStyle() function adds its argument as CSS code to the
// document.

// make CODE tags less visually salient
styleTag("CODE", "background-color: lightgrey");
styleTag("CODE", "color: grey");
// color things that occur in search results
styleDashTag("FLAG", "background-color: paleturquoise");
styleDashTag("XXX", "background-color: paleturquoise !important");
styleTag("ANT", "background-color: lightpink !important");
styleTag("CODING", "background-color: lightpink");
styleTag("TRACE", "background-color: paleturquoise");
styleTag("FLAG", "background-color: paleturquoise");
styleTag("CP", "background-color: lightsteelblue");
// color things that should be visually salient
styleTags(["FRAG","QTP","XP"], "background-color: darkseagreen");
styleTags(["VBPP","VBDP","VBNP","VBIP","VBSP","VBOP","VPRP","VPRP$","VPRPA","VPRPD"], "background-color: papayawhip");

/*
 * Phrase labels in this list (including the same ones with indices and
 * extensions) get a different background color so that the annotator can
 * see the "floor" of the current clause
 */

var ipnodes=["IP","RRC"];
styleIpNodes();

// Local Variables:
// indent-tabs-mode: nil
// End: