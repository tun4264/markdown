from ..parser import (
  ParserType,
  MarkdownParser,
)
import re

class Parser(MarkdownParser):
  def __init__(self) -> None:
    super().__init__()
    self.name:str = 'emphasis'
    self.reg_exp:re.Pattern = re.compile(r'\*(?P<text>.+?)\*')
    self.type:ParserType = ParserType.INLINE
  
  def parse(self, line:str) -> re.Match[str]|None:
    return self.reg_exp.search(line)

  def convert(self, lines:list[str]) -> str:
    result = '[parse error!]'
    if len(lines) != 1: return result
    text = lines[0]
    result = []
    i = 0
    while i < len(text):
      s = self.reg_exp.search(text, i)
      if s:
        start = s.start(0)
        end = start + len(s[0]) - 1
        result.append(text[i:start])
        result.append('<em>%(text)s</em>' % s.groupdict())
        i = end
      else:
        result.append(text[i:])
        break
      i += 1
    return ''.join(result)