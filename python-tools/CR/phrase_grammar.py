# Generated by the Waxeye Parser Generator - version 0.8.0
# www.waxeye.org

from waxeye import Edge, State, FA, WaxeyeParser

class Parser (WaxeyeParser):
    start = 0
    eof_check = True
    automata = [FA("tag", [State([Edge(3, 1, False),
                Edge(13, 3, False),
                Edge(2, 4, False)], False),
            State([Edge(1, 2, False)], True),
            State([], True),
            State([Edge(1, 2, False)], True),
            State([Edge(1, 2, False)], True)], FA.LEFT),
        FA("index", [State([Edge("-", 1, False),
                Edge("=", 1, False)], False),
            State([Edge([(48, 57)], 2, False)], False),
            State([Edge([(48, 57)], 2, False)], True)], FA.LEFT),
        FA("intermediate", [State([Edge("A", 1, False),
                Edge("I", 5, False),
                Edge("N", 6, False),
                Edge("A", 7, False),
                Edge("N", 10, False)], False),
            State([Edge("D", 2, False)], False),
            State([Edge("J", 3, False)], False),
            State([Edge("Y", 4, False)], False),
            State([], True),
            State([Edge("Y", 4, False)], False),
            State([Edge("Y", 4, False)], False),
            State([Edge("D", 8, False)], False),
            State([Edge("J", 9, False)], False),
            State([Edge("X", 4, False)], False),
            State([Edge("X", 4, False)], False)], FA.LEFT),
        FA("clause_tag", [State([Edge(5, 1, False),
                Edge(9, 1, False),
                Edge(4, 5, False)], False),
            State([Edge("-", 2, False)], True),
            State([Edge(11, 1, False),
                Edge(12, 3, False)], False),
            State([Edge("-", 4, False)], True),
            State([Edge(12, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("other", [State([Edge("F", 1, False),
                Edge("R", 5, False),
                Edge("Q", 7, False)], False),
            State([Edge("R", 2, False)], False),
            State([Edge("A", 3, False)], False),
            State([Edge("G", 4, False)], False),
            State([], True),
            State([Edge("R", 6, False)], False),
            State([Edge("C", 4, False)], False),
            State([Edge("T", 8, False)], False),
            State([Edge("P", 4, False)], False)], FA.LEFT),
        FA("ip", [State([Edge("I", 1, False)], False),
            State([Edge("P", 2, False)], False),
            State([Edge("-", 3, False)], True),
            State([Edge(6, 2, False)], False)], FA.LEFT),
        FA("ip_dash_tag", [State([Edge("A", 1, False),
                Edge("I", 4, False),
                Edge("M", 9, False),
                Edge("P", 11, False),
                Edge("S", 15, False)], False),
            State([Edge("B", 2, False)], False),
            State([Edge("S", 3, False)], False),
            State([], True),
            State([Edge("M", 5, False),
                Edge("N", 6, False)], False),
            State([Edge("P", 3, False)], False),
            State([Edge("F", 7, False)], False),
            State([Edge("-", 8, False)], True),
            State([Edge(7, 3, False)], False),
            State([Edge("A", 10, False)], False),
            State([Edge("T", 3, False)], False),
            State([Edge("P", 12, False)], False),
            State([Edge("L", 13, False)], False),
            State([Edge("-", 14, False)], True),
            State([Edge(8, 3, False)], False),
            State([Edge("M", 16, False),
                Edge("U", 17, False)], False),
            State([Edge("C", 3, False)], False),
            State([Edge("B", 3, False)], False)], FA.LEFT),
        FA("inf_type", [State([Edge("C", 1, False),
                Edge("P", 4, False),
                Edge("S", 6, False),
                Edge("T", 8, False),
                Edge("A", 10, False)], False),
            State([Edge("O", 2, False)], False),
            State([Edge("M", 3, False)], False),
            State([], True),
            State([Edge("R", 5, False)], False),
            State([Edge("P", 3, False)], False),
            State([Edge("B", 7, False)], False),
            State([Edge("J", 3, False)], False),
            State([Edge("H", 9, False)], False),
            State([Edge("T", 3, False)], False),
            State([Edge("B", 11, False)], False),
            State([Edge("S", 3, False)], False)], FA.LEFT),
        FA("ppl_type", [State([Edge("C", 1, False),
                Edge("T", 4, False)], False),
            State([Edge("O", 2, False)], False),
            State([Edge("M", 3, False)], False),
            State([], True),
            State([Edge("H", 5, False)], False),
            State([Edge("T", 3, False)], False)], FA.LEFT),
        FA("cp", [State([Edge("C", 1, False)], False),
            State([Edge("P", 2, False)], False),
            State([Edge("-", 3, False)], True),
            State([Edge(10, 2, False)], False)], FA.LEFT),
        FA("cp_dash_tag", [State([Edge("A", 1, False),
                Edge("C", 4, False),
                Edge("D", 8, False),
                Edge("E", 10, False),
                Edge("F", 13, False),
                Edge("P", 15, False),
                Edge("Q", 17, False),
                Edge("R", 19, False),
                Edge("T", 21, False)], False),
            State([Edge("D", 2, False)], False),
            State([Edge("V", 3, False)], False),
            State([], True),
            State([Edge("A", 5, False),
                Edge("O", 6, False),
                Edge("M", 7, False)], False),
            State([Edge("R", 3, False)], False),
            State([Edge("M", 3, False)], False),
            State([Edge("P", 3, False)], False),
            State([Edge("E", 9, False)], False),
            State([Edge("G", 3, False)], False),
            State([Edge("O", 11, False),
                Edge("X", 12, False)], False),
            State([Edge("P", 3, False)], False),
            State([Edge("L", 3, False)], False),
            State([Edge("R", 14, False)], False),
            State([Edge("L", 3, False)], False),
            State([Edge("R", 16, False)], False),
            State([Edge("P", 3, False)], False),
            State([Edge("U", 18, False)], False),
            State([Edge("E", 3, False)], False),
            State([Edge("E", 20, False)], False),
            State([Edge("L", 3, False),
                Edge("S", 3, False)], False),
            State([Edge("H", 22, False)], False),
            State([Edge("T", 3, False)], False)], FA.LEFT),
        FA("ext", [State([Edge("P", 1, False),
                Edge("S", 4, False)], False),
            State([Edge("R", 2, False)], False),
            State([Edge("N", 3, False)], False),
            State([], True),
            State([Edge("P", 5, False)], False),
            State([Edge("E", 3, False)], False)], FA.LEFT),
        FA("clause_dash_tag", [State([Edge("S", 1, False)], False),
            State([Edge("B", 2, False)], False),
            State([Edge("J", 3, False)], False),
            State([], True)], FA.LEFT),
        FA("phrase_tag", [State([Edge(18, 1, False),
                Edge(14, 1, False),
                Edge(15, 1, False),
                Edge(16, 1, False),
                Edge(17, 1, False),
                Edge(19, 1, False),
                Edge(20, 1, False)], False),
            State([Edge("-", 2, False)], True),
            State([Edge(11, 1, False)], False)], FA.LEFT),
        FA("np", [State([Edge("N", 1, False)], False),
            State([Edge("P", 2, False)], False),
            State([Edge("-", 3, False)], True),
            State([Edge("S", 4, False),
                Edge("O", 13, False),
                Edge("P", 15, False),
                Edge("A", 17, False),
                Edge("P", 19, False),
                Edge("C", 22, False),
                Edge("A", 25, False),
                Edge("D", 28, False),
                Edge("I", 30, False),
                Edge("L", 32, False),
                Edge("M", 34, False),
                Edge("S", 36, False),
                Edge("T", 38, False),
                Edge("V", 40, False),
                Edge("A", 42, False),
                Edge("C", 44, False),
                Edge("R", 8, False),
                Edge("L", 11, False)], False),
            State([Edge("B", 5, False)], False),
            State([Edge("J", 6, False)], False),
            State([Edge("-", 7, False)], True),
            State([Edge("R", 8, False),
                Edge("L", 11, False)], False),
            State([Edge("S", 9, False)], False),
            State([Edge("P", 10, False)], False),
            State([], True),
            State([Edge("F", 12, False)], False),
            State([Edge("D", 10, False)], False),
            State([Edge("B", 14, False)], False),
            State([Edge("1", 6, False),
                Edge("2", 6, False),
                Edge("P", 6, False),
                Edge("Q", 6, False)], False),
            State([Edge("R", 16, False)], False),
            State([Edge("D", 6, False)], False),
            State([Edge("T", 18, False)], False),
            State([Edge("R", 6, False)], False),
            State([Edge("R", 20, False),
                Edge("A", 21, False)], False),
            State([Edge("N", 6, False)], False),
            State([Edge("R", 6, False)], False),
            State([Edge("O", 23, False),
                Edge("M", 24, False)], False),
            State([Edge("M", 6, False)], False),
            State([Edge("P", 6, False)], False),
            State([Edge("D", 26, False),
                Edge("G", 27, False)], False),
            State([Edge("V", 6, False)], False),
            State([Edge("T", 6, False)], False),
            State([Edge("I", 29, False)], False),
            State([Edge("R", 6, False)], False),
            State([Edge("N", 31, False)], False),
            State([Edge("S", 6, False)], False),
            State([Edge("O", 33, False)], False),
            State([Edge("C", 6, False)], False),
            State([Edge("S", 35, False)], False),
            State([Edge("R", 6, False)], False),
            State([Edge("P", 37, False)], False),
            State([Edge("R", 6, False)], False),
            State([Edge("M", 39, False)], False),
            State([Edge("P", 6, False)], False),
            State([Edge("O", 41, False)], False),
            State([Edge("C", 6, False)], False),
            State([Edge("D", 43, False)], False),
            State([Edge("T", 6, False)], False),
            State([Edge("L", 6, False)], False)], FA.LEFT),
        FA("adjp", [State([Edge("A", 1, False)], False),
            State([Edge("D", 2, False)], False),
            State([Edge("J", 3, False)], False),
            State([Edge("P", 4, False)], False),
            State([Edge("-", 5, False)], True),
            State([Edge("P", 6, False),
                Edge("S", 9, False)], False),
            State([Edge("R", 7, False)], False),
            State([Edge("D", 8, False)], False),
            State([], True),
            State([Edge("P", 10, False)], False),
            State([Edge("R", 8, False)], False)], FA.LEFT),
        FA("advp", [State([Edge("A", 1, False)], False),
            State([Edge("D", 2, False)], False),
            State([Edge("V", 3, False)], False),
            State([Edge("P", 4, False)], False),
            State([Edge("-", 5, False)], True),
            State([Edge("D", 6, False),
                Edge("L", 9, False),
                Edge("T", 11, False)], False),
            State([Edge("I", 7, False)], False),
            State([Edge("R", 8, False)], False),
            State([], True),
            State([Edge("O", 10, False)], False),
            State([Edge("C", 8, False)], False),
            State([Edge("M", 12, False)], False),
            State([Edge("P", 8, False)], False)], FA.LEFT),
        FA("pp", [State([Edge("P", 1, False)], False),
            State([Edge("P", 2, False)], False),
            State([], True)], FA.LEFT),
        FA("nump", [State([Edge("N", 1, False)], False),
            State([Edge("U", 2, False)], False),
            State([Edge("M", 3, False)], False),
            State([Edge("P", 4, False)], False),
            State([], True)], FA.LEFT),
        FA("conjp", [State([Edge("C", 1, False)], False),
            State([Edge("O", 2, False)], False),
            State([Edge("N", 3, False)], False),
            State([Edge("J", 4, False)], False),
            State([Edge("P", 5, False)], False),
            State([], True)], FA.LEFT),
        FA("wh_phrase", [State([Edge("W", 1, False)], False),
            State([Edge("A", 2, False),
                Edge("N", 4, False),
                Edge("P", 4, False)], False),
            State([Edge("D", 3, False)], False),
            State([Edge("J", 4, False),
                Edge("V", 4, False)], False),
            State([Edge("P", 5, False)], False),
            State([], True)], FA.LEFT)]

    def __init__(self):
        WaxeyeParser.__init__(self, Parser.start, Parser.eof_check, Parser.automata)

