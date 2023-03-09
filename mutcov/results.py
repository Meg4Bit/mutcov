from typing import TypedDict

class Result(TypedDict):
    name: str
    score: int

def printResults(test: Test):
    return