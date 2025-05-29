import sys
from lex import *

class Parser():
    def __init__(self,lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()
        self.labelsDeclared = set()
        self.labelsGotoed = set()

        self.currentToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken() # Get the first two tokens for the peek

    def checkToken(self,kind):
        return kind == self.currentToken.kind

    def checkPeek(self,kind):
        return kind == self.peekToken.kind

    def match(self,kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.checkToken.kind.name)
        self.nextToken()
    
    def nextToken(self):
        self.currentToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def program(self):
        print("PROGRAM")
    
        self.emitter.emitHeader("#include <stdio.h>")
        self.emitter.emitHeader("int main() {")

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()
        
        for  label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Label " + label + " not declared")
        print("PROGRAM END")
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")
    # Checks all the grammar statements
    def statement(self):

        if self.checkToken(TokenType.PRINT):
            print("STATEMENT_PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine("printf(\"" + self.currentToken.text + "\\n\");")
                self.nextToken()
            else:
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")
        elif self.checkToken(TokenType.IF):
            print("STATEMENT_IF")
            self.nextToken()
            self.emitter.emit("if (")
            self.condition()
            self.match(TokenType.THEN)
            self.emitter.emitLine(") {")
            self.nl()

            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
            self.emitter.emitLine("}")

        elif self.checkToken(TokenType.WHILE):
            self.nextToken()
            self.emitter.emit("while (")
            self.condition()

            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine(") {")

            
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine("}")
            
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT_LABEL")
            self.nextToken()
            
            if self.currentToken.text in self.labelsDeclared:
                self.abort("Label " + self.currentToken.text + " already declared")
            self.labelsDeclared.add(self.currentToken.text)

            self.emitter.emitLine(self.currentToken.text + ":")
            self.match(TokenType.INDENT)

        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT_GOTO")
            self.nextToken()
            self.labelsGotoed.add(self.currentToken.text)
            self.emitter.emitLine("goto " + self.currentToken.text + ";")
            self.match(TokenType.INDENT)

        elif self.checkToken(TokenType.LET):
            print("STATEMENT_LET")
            self.nextToken()

            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)
                self.emitter.emitHeader("float " + self.currentToken.text + ";")

            self.emitter.emit(self.currentToken.text + " = ")
            self.match(TokenType.INDENT)
            self.match(TokenType.EQ)
            self.expression()
            self.emitter.emitLine(";")
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT_INPUT")
            self.nextToken()
            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)
                self.emitter.emitHeader("float " + self.currentToken.text + ";")
            
            self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.currentToken.text + ")) {")
            self.emitter.emitLine(self.currentToken.text + " = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emitLine("*s\");")
            self.emitter.emitLine("}")
            self.match(TokenType.INDENT)
        else:
            self.abort("Invalid Statement at "+ self.currentToken.text + "(" + self.currentToken.kind.name + ")")
        self.nl()
    
    def nl(self):
        print("NEWLINE")

        self.match(TokenType.NEWLINE)

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
    
    def condition(self):
        print("CONDITION")
        self.emitter.emit(self.currentToken.text)
        self.expression()

        if self.isConditionOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison at " + self.currentToken.text)
        
        while self.isConditionOperator():
            self.nextToken()
            self.expression()
    
    def isConditionOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.NOTEQ) or self.checkToken(TokenType.EQEQ)
    
    def expression(self):
        print("EXPRESSION")
        self.emitter.emit(self.currentToken.text)
        self.term()
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()
    def term(self):
        print("TERM")

        self.unary()
        while self.checkToken(TokenType.SLASH) or self.checkToken(TokenType.ASTERISK):
            self.nextToken()
            self.unary()
    
    def unary(self):
        print("UNARY")

        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    def primary(self):
        print("PRIMARY (" + self.currentToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.INDENT):

            if self.currentToken.text not in self.symbols:
                self.abort("Referenced variable before defined " + self.currentToken.text)
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.currentToken.text)
        
    def abort(self,message):
        sys.exit("Error - " + message)