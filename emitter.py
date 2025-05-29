import enum
import sys

class Emitter:
    def __init__(self, filename):
        self.file = filename
        self.header = ""
        self.code = ""
    
    def emit(self, code):
        self.code += code 
    
    def emitLine(self, code):
        self.code += code + "\n"

    def emitHeader(self, code):
        self.header += code + "\n"

    def WriteFile(self):
        with open(self.file, 'w') as outputFile:
            outputFile.write(self.header)
            outputFile.write(self.code)