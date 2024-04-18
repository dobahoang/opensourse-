from typing import Optional, Dict, Any


class ToolMessageChunk:
  def __init__(self, tool_call_id: str, content: Any, additional_kwargs: Optional[Dict] = None):
    self.tool_call_id = tool_call_id
    self.content = content
    self.additional_kwargs = additional_kwargs or {}  # Ensure empty dict if None

  def __add__(self, other: Any) -> "ToolMessageChunk":
    if not isinstance(other, ToolMessageChunk):
      raise TypeError("Can only add ToolMessageChunk objects")
    if self.tool_call_id != other.tool_call_id:
      raise ValueError("Cannot combine chunks with different tool call IDs")

    merged_content = merge_data(self.content, other.content)  # Custom function for merging tool-specific data
    merged_kwargs = {**self.additional_kwargs, **other.additional_kwargs}  # Combine dictionaries

    return ToolMessageChunk(
        tool_call_id=self.tool_call_id,
        content=merged_content,
        additional_kwargs=merged_kwargs,
    )

# Define merge_data function (example for keyword extraction):
def merge_data(content1, content2):
  merged_keywords = content1 +"___" + content2
  return merged_keywords

# Sample usage
chunk1 = ToolMessageChunk("keyword_tool", "apple", {"confidence": {"apple": 0.9}})
chunk2 = ToolMessageChunk("keyword_tool", "positive", {"score": 0.8})

combined_chunk = chunk1 + chunk2

print(combined_chunk.content)  # Output: ["apple", "banana", "positive"]
print(combined_chunk.additional_kwargs)  # Output: {"confidence": {"apple": 0.9}, "score": 0.8}
