import sys
import sqlite3
from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3Listener import Python3Listener


class CustomListener (Python3Listener):
    pathname:str = "\0"

    def PATHNAME (self):
        return self.pathname

    def __init__ (self, pathname, db, cursor):
        self.pathname = pathname
        self.db = db
        self.cursor = cursor

    IN:int = 0

    def enterFuncdef (self, ctx:Python3Parser.FuncdefContext):
        if self.IN == 0:
            print (self.pathname, ctx.DEF(), ctx.NAME())

            #self.cursor.execute ("SELECT file FROM objects")
            self.cursor.execute ("INSERT INTO objects (file, type, name) VALUES (\'{}\', \'{}\', \'{}\')".format (self.pathname, ctx.DEF(), ctx.NAME()))
            self.db.commit ()
        self.IN += 1

    def exitFuncdef (self, ctx:Python3Parser.FuncdefContext):
        self.IN -= 1

    def enterAsync_funcdef(self, ctx:Python3Parser.Async_funcdefContext):
        if self.IN == 0:
            print (self.pathname, ctx.ASYNC(), ctx.NAME())

            #self.cursor.execute ("SELECT file FROM objects")
            self.cursor.execute ("INSERT INTO objects (file, type, name) VALUES (\'{}\', \'{}\', \'{}\')".format (self.pathname, ctx.ASYNC(), ctx.NAME()))
            self.db.commit ()
        self.IN += 1

    def exitAsync_funcdef(self, ctx:Python3Parser.Async_funcdefContext):
        self.IN -= 1

    def enterClassdef (self, ctx:Python3Parser.ClassdefContext):
        if self.IN == 0:
            print (self.pathname, ctx.CLASS(), ctx.NAME())

            #self.cursor.execute ("SELECT file FROM objects")
            self.cursor.execute ("INSERT INTO objects (file, type, name) VALUES (\'{}\', \'{}\', \'{}\')".format (self.pathname, ctx.CLASS(), ctx.NAME()))
            self.db.commit ()
        self.IN += 1

    def exitClassdef (self, ctx:Python3Parser.ClassdefContext):
        self.IN -= 1


def initDB ():
    db = sqlite3.connect ('objects.db')
    cursor = db.cursor ()

    cursor.execute ("""CREATE TABLE IF NOT EXISTS objects (file TEXT, type TEXT, name TEXT)""")

    db.commit ()
    return db, cursor


# def FillBase (db, pathname):
#     input_stream = FileStream (pathname)
#     lexer = Python3Lexer (input_stream)
#     token_stream = CommonTokenStream (lexer)
#     parser = Python3Parser (token_stream)
#     tree = parser.file_input ()

#     handler = CustomListener ()
#     handler.IN = 0
#     walker = ParseTreeWalker ()
#     walker.walk (handler, tree)

#     cursor = db.cursor ()
#     cursor.execute ("SELECT file FROM objects")
#     cursor.execute ("INSERT INTO objects VALUES ('{path}')")


def PrintDB (cursor):
    for value in cursor.execute ("SELECT * FROM objects"):
        print (value)


def main ():
    db, cursor = initDB ()

    pathname = input ()
    input_stream = FileStream (pathname)
    lexer = Python3Lexer (input_stream)
    stream = CommonTokenStream (lexer)
    parser = Python3Parser (stream)
    tree = parser.file_input ()

    handler = CustomListener (pathname, db, cursor)
    handler.IN = 0
    walker = ParseTreeWalker ()
    walker.walk (handler, tree)

    PrintDB (cursor)

    db.close ()




if __name__ == '__main__':
    main ()