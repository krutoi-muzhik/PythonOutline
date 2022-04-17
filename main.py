import sys
from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3Listener import Python3Listener
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.startRule()
    enterer = FuncEnterer()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
 
class FuncEnterer (Python3Listener):
    def enterFuncdef(self, ctx:Python3Parser.FuncdefContext):
        print (self)

if __name__ == '__main__':
    main(sys.argv)