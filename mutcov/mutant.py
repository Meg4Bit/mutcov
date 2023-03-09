from testcase import Test

class Mutant(object):
    statement: str
    file: str
    code_line: int
    tests: list[Test]

    def __init__(self, file, line, statement):
        self.file = file
        self.code_line = line
        self.statement = statement
        
    def add(self):
        return 
      
    def execute(self):
        return



def createMutants(test: Test):
    return
