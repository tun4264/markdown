from ..parser import (
  ParserType,
  MarkdownParser,
)
import re

class Parser(MarkdownParser):
  def __init__(self) -> None:
    super().__init__()
    self.name:str = 'block_code'
    self.reg_exp:re.Pattern = re.compile(r'^```(?P<lang>.+)?')
    self.type:ParserType = ParserType.START_END_BLOCK
  
  def parse(self, line:str) -> re.Match[str]|None:
    return self.reg_exp.match(line)

  def convert(self, lines:list[str]) -> str:
    result = '[parse error!]'
    if len(lines) < 2: return result
    code_lines = lines[1:-1]
    match = self.reg_exp.match(lines[0])
    if match:
      mgd = match.groupdict()
      class_name = 'lang-%s' % (mgd['lang']) if mgd.get('lang', None) else ''
      result = '<pre><code class="%(class)s">%(text)s</code></pre>' % {'class': class_name, 'text': '\r\n'.join(code_lines)}
    return result