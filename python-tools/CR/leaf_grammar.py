# Generated by the Waxeye Parser Generator - version 0.8.0
# www.waxeye.org

from waxeye import Edge, State, FA, WaxeyeParser

class Parser (WaxeyeParser):
    start = 0
    eof_check = True
    automata = [FA("word_tag", [State([Edge(1, 1, False),
                Edge(3, 1, False),
                Edge(9, 1, False),
                Edge(10, 1, False),
                Edge(11, 1, False),
                Edge(12, 1, False),
                Edge(13, 1, False)], False),
            State([], True)], FA.LEFT),
        FA("nominal", [State([Edge("N", 1, False),
                Edge("A", 6, False),
                Edge("D", 9, False),
                Edge("N", 11, False),
                Edge("P", 13, False),
                Edge("Q", 16, False),
                Edge("O", 17, False)], False),
            State([Edge("P", 2, False),
                Edge("S", 4, False),
                Edge(2, 5, False)], False),
            State([Edge("R", 3, False)], False),
            State([Edge("S", 4, False),
                Edge(2, 5, False)], False),
            State([Edge(2, 5, False)], False),
            State([], True),
            State([Edge("D", 7, False)], False),
            State([Edge("J", 8, False)], False),
            State([Edge("R", 5, False),
                Edge("S", 5, False),
                Edge(2, 5, False)], True),
            State([Edge("S", 10, False),
                Edge(2, 5, False)], False),
            State([Edge(2, 5, False)], False),
            State([Edge("U", 12, False)], False),
            State([Edge("M", 5, False)], False),
            State([Edge("R", 14, False)], False),
            State([Edge("O", 15, False)], False),
            State([Edge(2, 5, False)], False),
            State([Edge("R", 5, False),
                Edge("S", 5, False),
                Edge(2, 5, False)], True),
            State([Edge("T", 18, False)], False),
            State([Edge("H", 19, False)], False),
            State([Edge("E", 20, False)], False),
            State([Edge("R", 21, False)], False),
            State([Edge(2, 5, False)], False)], FA.LEFT),
        FA("case", [State([Edge("-", 1, False)], False),
            State([Edge("N", 2, False),
                Edge("G", 5, False),
                Edge("A", 7, False),
                Edge("D", 9, False)], False),
            State([Edge("O", 3, False)], False),
            State([Edge("M", 4, False)], False),
            State([], True),
            State([Edge("E", 6, False)], False),
            State([Edge("N", 4, False)], False),
            State([Edge("C", 8, False)], False),
            State([Edge("C", 4, False)], False),
            State([Edge("A", 10, False)], False),
            State([Edge("T", 4, False)], False)], FA.LEFT),
        FA("verbal", [State([Edge(4, 1, False),
                Edge(5, 1, False)], False),
            State([], True)], FA.LEFT),
        FA("verb", [State([Edge("B", 1, False),
                Edge("V", 8, False)], False),
            State([Edge("E", 2, False)], False),
            State([Edge("P", 3, False),
                Edge("D", 3, False),
                Edge("I", 3, False),
                Edge("N", 3, False),
                Edge("O", 3, False),
                Edge("S", 3, False)], False),
            State([Edge("P", 4, False),
                Edge(6, 5, False)], False),
            State([Edge(6, 5, False)], False),
            State([Edge(7, 6, False),
                Edge(8, 7, False)], True),
            State([Edge(8, 7, False)], True),
            State([], True),
            State([Edge("B", 2, False)], False)], FA.LEFT),
        FA("participle", [State([Edge("B", 1, False),
                Edge("V", 8, False)], False),
            State([Edge("P", 2, False)], False),
            State([Edge("R", 3, False)], False),
            State([Edge("P", 4, False),
                Edge(6, 5, False)], False),
            State([Edge(6, 5, False)], False),
            State([Edge(7, 6, False),
                Edge(2, 7, False)], False),
            State([Edge(2, 7, False)], False),
            State([], True),
            State([Edge("P", 9, False)], False),
            State([Edge("R", 3, False)], False)], FA.LEFT),
        FA("aspect", [State([Edge("-", 1, False)], False),
            State([Edge("A", 2, False),
                Edge("F", 5, False),
                Edge("I", 7, False),
                Edge("P", 10, False)], False),
            State([Edge("O", 3, False)], False),
            State([Edge("R", 4, False)], False),
            State([], True),
            State([Edge("U", 6, False)], False),
            State([Edge("T", 4, False)], False),
            State([Edge("M", 8, False)], False),
            State([Edge("P", 9, False)], False),
            State([Edge("F", 4, False)], False),
            State([Edge("R", 11, False)], False),
            State([Edge("F", 4, False)], False)], FA.LEFT),
        FA("voice", [State([Edge("-", 1, False)], False),
            State([Edge("P", 2, False),
                Edge("I", 6, False),
                Edge("T", 11, False)], False),
            State([Edge("A", 3, False)], False),
            State([Edge("S", 4, False)], False),
            State([Edge("S", 5, False)], False),
            State([], True),
            State([Edge("N", 7, False)], False),
            State([Edge("T", 8, False)], False),
            State([Edge("R", 9, False)], False),
            State([Edge("N", 10, False)], False),
            State([Edge("S", 5, False)], False),
            State([Edge("R", 12, False)], False),
            State([Edge("N", 13, False)], False),
            State([Edge("S", 14, False)], False),
            State([Edge("1", 5, False),
                Edge("2", 5, False)], False)], FA.LEFT),
        FA("opt", [State([Edge("-", 1, False)], False),
            State([Edge("K", 2, False),
                Edge("I", 5, False)], False),
            State([Edge("J", 3, False)], False),
            State([Edge("V", 4, False)], False),
            State([], True),
            State([Edge("N", 6, False)], False),
            State([Edge("D", 4, False)], False)], FA.LEFT),
        FA("adverb", [State([Edge("A", 1, False),
                Edge("N", 5, False),
                Edge("Q", 7, False)], False),
            State([Edge("D", 2, False)], False),
            State([Edge("V", 3, False)], False),
            State([Edge("R", 4, False),
                Edge("S", 4, False)], True),
            State([], True),
            State([Edge("E", 6, False)], False),
            State([Edge("G", 4, False)], False),
            State([Edge("V", 4, False)], False)], FA.LEFT),
        FA("clitic", [State([Edge("C", 1, False)], False),
            State([Edge("L", 2, False)], False),
            State([Edge("G", 3, False),
                Edge("P", 5, False),
                Edge("Q", 8, False),
                Edge("P", 9, False),
                Edge("T", 11, False)], True),
            State([Edge("E", 4, False)], False),
            State([], True),
            State([Edge("R", 6, False)], False),
            State([Edge("O", 7, False)], False),
            State([Edge(2, 4, False)], True),
            State([Edge(2, 4, False)], True),
            State([Edge("R", 10, False)], False),
            State([Edge("T", 4, False)], False),
            State([Edge("E", 4, False)], False)], FA.LEFT),
        FA("fn_cat", [State([Edge("A", 1, False),
                Edge("K", 3, False),
                Edge("I", 4, False),
                Edge("P", 7, False),
                Edge("C", 10, False),
                Edge("P", 2, False),
                Edge("W", 13, False)], False),
            State([Edge("N", 2, False)], False),
            State([], True),
            State([Edge("E", 2, False)], False),
            State([Edge("N", 5, False)], False),
            State([Edge("T", 6, False)], False),
            State([Edge("J", 2, False)], False),
            State([Edge("R", 8, False)], False),
            State([Edge("T", 9, False)], False),
            State([Edge("Q", 2, False)], False),
            State([Edge("O", 11, False)], True),
            State([Edge("N", 12, False)], False),
            State([Edge("J", 2, False)], False),
            State([Edge("A", 14, False),
                Edge("D", 2, False),
                Edge("P", 17, False),
                Edge("Q", 2, False)], False),
            State([Edge("D", 15, False)], False),
            State([Edge("J", 16, False),
                Edge("V", 2, False)], False),
            State([Edge(2, 2, False)], False),
            State([Edge("R", 18, False)], True),
            State([Edge("O", 19, False)], False),
            State([Edge(2, 2, False)], False)], FA.LEFT),
        FA("other_word", [State([Edge("C", 1, False),
                Edge("F", 5, False),
                Edge("X", 4, False),
                Edge("Y", 4, False)], False),
            State([Edge("O", 2, False)], False),
            State([Edge("D", 3, False)], False),
            State([Edge("E", 4, False)], False),
            State([], True),
            State([Edge("W", 4, False)], False)], FA.LEFT),
        FA("punct", [State([Edge("\"", 1, False),
                Edge(",", 1, False),
                Edge(".", 1, False),
                Edge("L", 2, False),
                Edge("R", 7, False)], False),
            State([], True),
            State([Edge("P", 3, False)], False),
            State([Edge("A", 4, False)], False),
            State([Edge("R", 5, False)], False),
            State([Edge("E", 6, False)], False),
            State([Edge("N", 1, False)], False),
            State([Edge("P", 8, False)], False),
            State([Edge("A", 9, False)], False),
            State([Edge("R", 10, False)], False),
            State([Edge("E", 11, False)], False),
            State([Edge("N", 1, False)], False)], FA.LEFT)]

    def __init__(self):
        WaxeyeParser.__init__(self, Parser.start, Parser.eof_check, Parser.automata)

