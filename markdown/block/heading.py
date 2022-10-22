from ..parser import (
  ParserType,
  MarkdownParser,
)
import re

class Parser(MarkdownParser):
  def __init__(self) -> None:
    super().__init__()
    self.name:str = 'h'
    self.reg_exp:re.Pattern = re.compile(r'^(?P<level>#{1,6}) (?P<text>.+)')
    self.type:ParserType = ParserType.SINGLE_LINE_BLOCK
  
  def convert(self, lines:list[str]) -> str:
    result = '[parse error!]'
    if len(lines) != 1: return result
    match = self.reg_exp.match(lines[0])
    if match:
      mgd = match.groupdict()
      result = '<h%(level)d>%(text)s</h%(level)d>' % {'level': len(mgd['level']), 'text': mgd['text']}
    return result