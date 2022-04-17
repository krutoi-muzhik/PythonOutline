import sys
from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3Listener import Python3Listener
 
class FuncClassHandler (Python3Listener):
    def enterFuncdef(self, ctx:Python3Parser.FuncdefContext):
        print ("function ", ctx.NAME())
        
    def enterClassdef(self, ctx:Python3Parser.ClassdefContext):
        print ("class ", ctx.NAME())
 
def main(argv):
    input_stream = FileStream (argv[1])
    lexer = Python3Lexer (input_stream)
    stream = CommonTokenStream (lexer)
    parser = Python3Parser (stream)
    tree = parser.file_input ()

    handler = FuncClassHandler ()
    walker = ParseTreeWalker ()
    walker.walk (handler, tree)

if __name__ == '__main__':
    main(sys.argv)