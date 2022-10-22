from enum import Enum
import re

class ParserType(Enum):
  INLINE = 0
  SINGLE_LINE_BLOCK = 1
  MULTIPLE_LINE_BLOCK = 2
  START_END_BLOCK = 3
    

class MarkdownParser(object):
  def __init__(self) -> None:
    self.name:str = 'none'
    self.reg_exp:re.Pattern = None
    self.type:ParserType = None

  def parse(self, line:str) -> re.Match[str]|None:
    return self.reg_exp.match(line)
  
  def convert(self, lines:list[str]) -> str:
    return ''