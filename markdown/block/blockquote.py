from ..parser import (
  ParserType,
  MarkdownParser,
)
import re

class Parser(MarkdownParser):
  def __init__(self) -> None:
    super().__init__()
    self.name:str = 'blockquote'
    self.reg_exp:re.Pattern = re.compile(r'^> (?P<text>.+)')
    self.type:ParserType = ParserType.MULTIPLE_LINE_BLOCK
  
  def convert(self, lines:list[str]) -> str:
    result = '[parse error!]'
    if len(lines) == 0: return result
    ulli = []
    for line in lines:
      match = self.reg_exp.match(line)
      if match:
        ulli.append('<p>%(text)s</p>' % match.groupdict())
    return '<blockquote>%s</blockquote>' % (''.join(ulli))