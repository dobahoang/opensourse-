"""Base callback handler that can be used to handle callbacks in langchain."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, TypeVar, Union
from uuid import UUID

from tenacity import RetryCallState

if TYPE_CHECKING:
    from core.langchain_core.agents import AgentAction, AgentFinish
    from core.langchain_core.documents import Document
    from core.langchain_core.messages import BaseMessage
    from core.langchain_core.outputs import ChatGenerationChunk, GenerationChunk, LLMResult
