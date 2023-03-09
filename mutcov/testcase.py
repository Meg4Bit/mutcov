import re
import os
import time
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import List
from pytest import Session, Config, PytestPluginManager

class Test(object):
    name: str
    execution_time: time.struct_time 
    _coverage = []

    def __init__(self, name):
        self.name = name
        
    @property
    def coverage(self):
        return self._coverage

    @coverage.setter       
    def coverage(self, cov):
        self._coverage = cov

def readTests(dirs  : List[Path]) -> List[Test]:
    
    session = Session.from_config()
    tests: list[Test] = []
    files = os.listdir(dir)
    for file in files:
        if re.search(".py$", file):
            tests.append(Test(file))
    return tests

def runCoverage(test: Test):
    return
