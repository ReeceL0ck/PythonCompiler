import sys
from lex import *

class Parser():
    def __init__(self,lexer):
        self.lexer = lexer

        self.currentToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

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

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()
    # Checks all the grammar statements
    def statement(self):

        if self.checkToken(TokenType.PRINT):
            print("STATEMENT_PRINT")
            self.nextToken()
        
            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()
        elif self.checkToken(TokenType.IF):
            print("STATEMENT_IF")
            self.nextToken()
            self.condition()
            self.match(TokenType.THEN)
            self.nl()

            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)

        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT_WHILE")
            self.nextToken()
            self.condition()
            self.match(TokenType.REPEAT)
            self.nl()
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
        
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT_LABEL")
            self.nextToken()
            self.match(TokenType.INDENT)

        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT_GOTO")
            self.nextToken()
            self.match(TokenType.INDENT)

        elif self.checkToken(TokenType.LET):
            print("STATEMENT_LET")
            self.nextToken()
            self.match(TokenType.INDENT)
            self.match(TokenType.EQ)
            self.expression()

        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT_INPUT")
            self.nextToken()
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
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.currentToken.text)
        
    def abort(self,message):
        sys.exit("Error" + message)