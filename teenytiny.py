from emitter import *
from lex import * 
from parse import *
import sys

def main():
    print("Teeny Tiny compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs a source file")
    with open(sys.argv[1],'r') as inputFile:
        source = inputFile.read()

    lexer = Lexer(source)
    emitter = Emitter('out.c')
    parser = Parser(lexer, emitter=emitter)

    parser.program()
    emitter.WriteFile()
    print("Compiling Done")
    

main()