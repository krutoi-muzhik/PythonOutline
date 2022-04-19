import sys
import sqlite3

from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3Listener import Python3Listener
from Python3Visitor import Python3Visitor


class CustomVisitor (Python3Visitor):
    def __init__ (self, pathname, db, cursor):
        self.IN:int = 0
        self.pathname = pathname
        self.db = db
        self.cursor = cursor

    def PATHNAME (self):
        return self.pathname

    def visitFuncdef(self, ctx:Python3Parser.FuncdefContext):
        if self.IN == 0:
            self.cursor.execute ('''INSERT INTO objects (file, type, name, startline, endline)
                                    VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'''.format (self.pathname, ctx.DEF(), ctx.NAME(), ctx.start.line, ctx.stop.line))


        self.IN += 1
        self.visitChildren(ctx)
        self.IN -= 1

    def visitClassdef(self, ctx:Python3Parser.ClassdefContext):
        if self.IN == 0:
            self.cursor.execute ('''INSERT INTO objects (file, type, name, startline, endline) 
                                    VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'''.format (self.pathname, ctx.CLASS(), ctx.NAME(), ctx.start.line, ctx.stop.line))

        self.IN += 1
        self.visitChildren(ctx)
        self.IN -= 1


class CustomListener (Python3Listener):
    def __init__ (self, pathname, db, cursor):
        self.pathname = pathname
        self.db = db
        self.cursor = cursor

    def PATHNAME (self):
        return self.pathname

    def enterFuncdef (self, ctx:Python3Parser.FuncdefContext):
        if self.IN == 0:
            #self.cursor.execute ("SELECT file FROM objects")
            #print ("start = ", ctx.start.line, "stop = ", ctx.stop.line)
            self.cursor.execute ('''INSERT INTO objects (file, type, name, startline, endline) 
                                    VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'''.format (self.pathname, ctx.DEF(), ctx.NAME(), ctx.start.line, ctx.stop.line))
            self.db.commit ()
        self.IN += 1

    def exitFuncdef (self, ctx:Python3Parser.FuncdefContext):
        self.IN -= 1

    def enterAsync_funcdef(self, ctx:Python3Parser.Async_funcdefContext):
        if self.IN == 0:
            #self.cursor.execute ("SELECT file FROM objects")
            #print ("start = ", ctx.start.line, "stop = ", ctx.stop.line)
            self.cursor.execute ('''INSERT INTO objects (file, type, name, startline, endline) 
                                    VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'''.format (self.pathname, ctx.ASYNC(), ctx.NAME(), ctx.start.line, ctx.stop.line))
            self.db.commit ()
        self.IN += 1

    def exitAsync_funcdef(self, ctx:Python3Parser.Async_funcdefContext):
        self.IN -= 1

    def enterClassdef (self, ctx:Python3Parser.ClassdefContext):
        if self.IN == 0:
            #self.cursor.execute ("SELECT file FROM objects")
            #print ("start = ", ctx.start.line, "stop = ", ctx.stop.line)
            self.cursor.execute ('''INSERT INTO objects (file, type, name, startline, endline) 
                                    VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'''.format (self.pathname, ctx.CLASS(), ctx.NAME(), ctx.start.line, ctx.stop.line))
            self.db.commit ()
        self.IN += 1

    def exitClassdef (self, ctx:Python3Parser.ClassdefContext):
        self.IN -= 1


def initDB (pathname):
    db = sqlite3.connect (pathname)
    cursor = db.cursor ()

    cursor.execute ('''CREATE TABLE IF NOT EXISTS objects (file TEXT, type TEXT, name TEXT, startline TEXT, endline TEXT)''')

    db.commit ()
    return db, cursor


def PrintDB (cursor):
    for value in cursor.execute ("SELECT * FROM objects"):
        print (value)


def ParseFile (pathname):
    input_stream = FileStream (pathname)
    lexer = Python3Lexer (input_stream)
    stream = CommonTokenStream (lexer)
    parser = Python3Parser (stream)
    return parser.file_input ()


def ListenFile (pathname, db, cursor):
    tree = ParseTree (pathname)
    handler = CustomListener (pathname, db, cursor)
    handler.IN = 0
    walker = ParseTreeWalker ()
    walker.walk (handler, tree)


def VisitFile (pathname, db, cursor):
    tree = ParseFile (pathname)
    visitor = CustomVisitor(pathname, db, cursor)
    visitor.visit(tree)


def main ():
    db, cursor = initDB ('objects.db')

    paths = input ()
    for value in paths.split(" "):
        if value != "":
            VisitFile (value, db, cursor)

    PrintDB (cursor)

    db.close ()



if __name__ == '__main__':
    main ()
