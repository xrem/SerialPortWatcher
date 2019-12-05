# HACK: This imports here just to allow access to the top-level directory of project.
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..', '..'))

from models.InputPortKind import InputPortKind
from core.parsers.AbstractParser import AbstractParser
from core.parsers.FromFreezerParser import FromFreezerParser
from core.parsers.FromTerminalParser import FromTerminalParser

class Factory():
    @staticmethod
    def createParser(kind: InputPortKind) -> AbstractParser:
        if kind == kind.Freezer:
            return FromFreezerParser()
        elif kind == kind.Terminal:
            return FromTerminalParser()
