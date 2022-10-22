from ..parser import (
  ParserType,
  MarkdownParser,
)
import re

class Parser(MarkdownParser):
  def __init__(self) -> None:
    super().__init__()
    self.name:str = 'hr'
    self.reg_exp:re.Pattern = re.compile(r'^---')
    self.type:ParserType = ParserType.SINGLE_LINE_BLOCK

  def convert(self, lines:list[str]) -> str:
    return '<hr>'