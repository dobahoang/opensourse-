from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from core.langchain_core.messages.ai import (
    AIMessage,
    AIMessageChunk,
)
from core.langchain_core.messages.base import (
    BaseMessage,
    BaseMessageChunk,
)
from core.langchain_core.messages.chat import ChatMessage, ChatMessageChunk
from core.langchain_core.messages.function import FunctionMessage, FunctionMessageChunk
from core.langchain_core.messages.human import HumanMessage, HumanMessageChunk
from core.langchain_core.messages.system import SystemMessage, SystemMessageChunk
from core.langchain_core.messages.tool import ToolMessage, ToolMessageChunk

AnyMessage = Union[
    AIMessage, HumanMessage, ChatMessage, SystemMessage, FunctionMessage, ToolMessage
]

def get_buffer_string(
        messages: Sequence[BaseMessage], human_prefix: str = "Human", ai_prefix: str = "AI"
) -> str:
    """Convert a sequence of Messages to strings and concatenate them into one string.

     Args:
         messages: Messages to be converted to strings.
         human_prefix: The prefix to prepend to contents of HumanMessages.
         ai_prefix: THe prefix to prepend to contents of AIMessages.

     Returns:
         A single string concatenation of all input messages.

     Example:
         .. code-block:: python

             from langchain_core import AIMessage, HumanMessage

             messages = [
                 HumanMessage(content="Hi, how are you?"),
                 AIMessage(content="Good, how are you?"),
             ]
             get_buffer_string(messages)
             # -> "Human: Hi, how are you?\nAI: Good, how are you?"
     """
    string_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            role = human_prefix
        elif isinstance(m, AIMessage):
            role = ai_prefix
        elif isinstance(m, SystemMessage):
            role = "System"
        elif isinstance(m, FunctionMessage):
            role = "Function"
        elif isinstance(m, ToolMessage):
            role = "Tool"
        elif isinstance(m, ChatMessage):
            role = m.role
        else:
            raise ValueError(f"Got unsupported message type : {m}")
        messages = f"{role}: {m.content}"
        if isinstance(m, AIMessage) and "function_call" in m.additional_kwargs:
            messages += f" ({m.additional_kwargs['function_call']})"
        string_messages.append(messages)

    return "\n".join(string_messages)

def _message_from_dict(message: dict) -> BaseMessage:
    _type = message["type"]
    if _type == "human":
        return HumanMessage(**message["data"])
    elif _type == "ai":
        return AIMessage(**message["data"])
    elif _type == "system":
        return SystemMessage(**message["data"])
    elif _type == "function":
        return FunctionMessage(**message["data"])
    elif _type == "tool":
        return ToolMessage(**message["data"])
    elif _type == "AIMessageChunk":
        return AIMessageChunk(**message["data"])
    elif _type == "HumanMessageChunk":
        return HumanMessageChunk(**message["data"])
    elif _type == "FunctionMessageChunk":
        return FunctionMessageChunk(**message["data"])
    elif _type == "ToolMessageChunk":
        return ToolMessageChunk(**message["data"])
    elif _type == "SystemMessageChunk":
        return SystemMessageChunk(**message["data"])
    elif _type == "ChatMessageChunk":
        return ChatMessageChunk(**message["data"])
    else:
        raise ValueError(f"Got unsupported message type : {_type}")

def message_chunk_to_message(chunk: BaseMessageChunk) -> BaseMessage:
    """Convert a message chunk to a message
    Args:
        chunk: Message chunk to convert

    Returns:
        Message.
    """

    if not isinstance(chunk, BaseMessageChunk):
        return chunk

#     chunk classe always have the equivalent non-chunk class as their first parent
    ignore_keys = ["type"]
    if isinstance(chunk, AIMessageChunk):
        ignore_keys.append("tool_call_chunks")
    return chunk.__class__.__mro__[1](**{k: v for k, v in chunk.dict().items() if k not in ignore_keys})




