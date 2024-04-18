from typing import Any, Dict, List, Literal

from langchain_core.messages.base import (
    BaseMessage,
    BaseMessageChunk,
    merge_content,
)
from langchain_core.messages.tool import (
    InvalidToolCall,
    ToolCall,
    ToolCallChunk,
    default_tool_chunk_parser,
    default_tool_parser,
)
from langchain_core.pydantic_v1 import root_validator
from langchain_core.utils._merge import merge_dicts, merge_lists
from langchain_core.utils.json import (
    parse_partial_json,
)


class AIMessage(BaseMessage):
    """Message from AI."""

    example: bool = False
    """Whether this Message is being passed in to the model as part of an example conversation."""

    tool_calls: List[ToolCall] = []
    """If provided , tool calls associated with the message """

    invalid_tool_calls: List[InvalidToolCall] = []
    """If  provided, tool calls with parsing errors associated with the message."""

    type: Literal["ai"] = "ai"

    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object"""
        return ["langchain", "schema", "messages"]

    @property
    def lc_attributes(self) -> Dict:
        """Attrs to be serialized even if they are derived from other init args"""

        return {
            "tool_calls": self.tool_calls,
            "invalid_tool_calls": self.invalid_tool_calls
        }











