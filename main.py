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

            print ("ARROW = ", ctx.ARROW(), "")

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


def initDB (pathname):
    db = sqlite3.connect (pathname)
    cursor = db.cursor ()

    cursor.execute ("""CREATE TABLE IF NOT EXISTS objects (file TEXT, type TEXT, name TEXT)""")

    db.commit ()
    return db, cursor


def PrintDB (cursor):
    for value in cursor.execute ("SELECT * FROM objects"):
        print (value)


def ListenFile (pathname, db, cursor):
    input_stream = FileStream (pathname)
    lexer = Python3Lexer (input_stream)
    stream = CommonTokenStream (lexer)
    parser = Python3Parser (stream)
    tree = parser.file_input ()

    handler = CustomListener (pathname, db, cursor)
    handler.IN = 0
    walker = ParseTreeWalker ()
    walker.walk (handler, tree)


def main ():
    db, cursor = initDB ('objects.db')

    paths = input ()
    for value in paths.split(" "):
        if value != "":
            ListenFile (value, db, cursor)

    PrintDB (cursor)

    db.close ()



if __name__ == '__main__':
    main ()
