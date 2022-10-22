
from typing import *
from . import parser as mdp
from .block import (
  block_code,
  heading,
  unordered_list,
  ordered_list,
  blockquote,
  horizontal_rule,
)
from .inline import (
  anchor,
  inline_code,
  image,
  strong,
  emphasis,
)

class Markdown(object):
  def __init__(self) -> None:
    self.parsers:list[mdp.MarkdownParser] = [
      heading.Parser(),
      ordered_list.Parser(),
      unordered_list.Parser(),
      blockquote.Parser(),
      block_code.Parser(),
      horizontal_rule.Parser(),
      image.Parser(),
      anchor.Parser(),
      inline_code.Parser(),
      strong.Parser(),
      emphasis.Parser(),
    ]
    self.context:dict = {
      'opened': None,
      'type': None,
      'start': None,
    }
  
  def _find_line_end(self, text:str) -> str:
    for end in ['\r\n', '\n', '\r']:
      if text.find(end) != -1:
        return end
    return '\r\n'
  
  def _find_block_parser(self, line:str) -> mdp.MarkdownParser:
    block_parsers:list[mdp.MarkdownParser] = filter(lambda parser: parser.type is not mdp.ParserType.INLINE, self.parsers)
    for parser in block_parsers:
      match = parser.parse(line)
      if match:
        return parser
    return None

  def _convert_inline(self, line:str):
    inline_parsers:list[mdp.MarkdownParser] = filter(lambda parser: parser.type is mdp.ParserType.INLINE, self.parsers)
    for parser in inline_parsers:
      line = parser.convert([line])
    return line

  def to_html(self, markdown:str):
    line_end = self._find_line_end(markdown)
    lines = markdown.split(line_end)
    num_of_lines = len(lines)
    html_lines = []
    old_parser = None
    # 解析のメインループ
    for cursor in range(0, num_of_lines, 1):
      current_line = lines[cursor]
      parser = self._find_block_parser(current_line)
      if parser:
        # ブロックの一部を発見した場合
        if not self.context['opened']:
          # ブロックは開いていない場合
          if parser.type == mdp.ParserType.SINGLE_LINE_BLOCK:
            html_lines.append(parser.convert(lines[cursor:cursor + 1]))
            self.context['type'] = self.context['opened'] = self.context['start'] = None
          else:
            self.context['type'] = parser.type
            self.context['opened'] = parser.name
            self.context['start'] = cursor
        elif self.context['opened'] == parser.name:
          # ブロックは既に開いていて、現在の行で閉じた場合
          if self.context['type'] == mdp.ParserType.START_END_BLOCK:
            html_lines.append(parser.convert(lines[self.context['start']:cursor + 1]))
            self.context['type'] = self.context['opened'] = self.context['start'] = None
          else:
            self.context['type'] = parser.type
            self.context['opened'] = parser.name
        else:
          # ブロックは既に開いていて、別のブロックを見つけた場合
          html_lines.append(parser.convert(lines[self.context['start']:cursor]))
          self.context['type'] = parser.type
          self.context['opened'] = parser.name
          self.context['start'] = cursor
        old_parser = parser
      else:
        # ブロックが発見できなかった場合
        if self.context['type'] == mdp.ParserType.START_END_BLOCK:
          # ブロックの中身は処理を無視する
          pass
        else:
          # 通常のテキスト（<p>タグとして処理）
          if self.context['opened'] and self.context['start']:
            html_lines.append(old_parser.convert(lines[self.context['start']:cursor]))
          if current_line != '':
            html_lines.append('<p>%s</p>' % (self._convert_inline(current_line)))
          self.context['type'] = self.context['opened'] = self.context['start'] = None
    return '\r\n'.join(html_lines)
  