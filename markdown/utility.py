from typing import *

def list_filter(target:list|set, func:Callable[[Any, int, list|set], bool], first=False) -> Any:
  result = []
  for i in range(0, len(target)):
    if func(target[i], i, target) and not first:
      result.append(target[i])
    elif func(target[i], i, target) and first:
      return target[i]
    else:
      continue
  return result