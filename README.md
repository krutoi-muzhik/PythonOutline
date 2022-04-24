# Intro

This programm is a simple Python Outline, that finds every defenition of a global function or class in input python files.

# Run

To run this programm, you should have python3 and sqlite3 library for python installed on your PC

If you want to generate [lexer](https://github.com/krutoi-muzhik/PythonOutline/blob/main/Python3Lexer.py) and [parser](https://github.com/krutoi-muzhik/PythonOutline/blob/main/Python3Parser.py) by yourself, you should install Java, ANTLR4 and ANTLR4 library for python runtime, and then use:

	antlr4 -Dlanguage=Python3 Python3.g4

If you want to generate [listener](https://github.com/krutoi-muzhik/PythonOutline/blob/main/Python3Listener.py), you can just use the command above, but if you want to generate [visitor](https://github.com/krutoi-muzhik/PythonOutline/blob/main/Python3Visitor.py), you should add flag. 

	-visitor 

##### If you want to find out the difference between listener and visitor, read about the implementation below

# Implementation 

Not to remember the whole python grammar and code lexer and parser by myself, I used ANTLR4 tool, that generates parser, lexer, visitor and listener classes for the grammar that is written in Python3.g4 file.

## Parser and lexer

Parser and lexer generated by antlr handle tasks we need well, so we don't need to change anything.

## Listener

To listen all the nodes of parsed AST tree, we use standart antlr walker, that recusirsively walks through all the nodes and starts listener according to the type of the node.

To remember the filename, set database output and avoid recreating of cursor, we transfer "pathname" "db" and "cursor" to our listener class:

```Python
class CustomListener (Python3Listener):
    def __init__ (self, pathname, db, cursor):
        self.pathname = pathname
        self.db = db
        self.cursor = cursor

    def PATHNAME (self):
        return self.pathname

```

As we need to print functions and classes, we need to overload the appropriate methods in listener class. This is how it looks:

```Python
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
```

The field "IN" we need to count, how many times we entered functions or classes defenitions. We use it to find out if the object is global or defined inside another object.

## Visitor

Here we save needed variables in visitor class, as we implemented it in listener above:

```Python
class CustomVisitor (Python3Visitor):
    def __init__ (self, pathname, db, cursor):
        self.IN:int = 0
        self.pathname = pathname
        self.db = db
        self.cursor = cursor

    def PATHNAME (self):
        return self.pathname
```

The main difference between listener and visitor is that we don't use default walker in visitor. To recursively walk through the tree, we should start visit function for node's children every time we visit a new node.

This is how our visitor methods for functiions and classes must be overloaded:

```Python
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
```

Here we also use the field "IN" to save only global objects.