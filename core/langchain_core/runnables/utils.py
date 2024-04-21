import ast
import asyncio
import inspect
import textwrap
from functools import lru_cache
from inspect import signature
from itertools import groupby
from typing import (
    Any,
    AsyncIterable,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
)

from core.langchain_core.pydantic_v1 import BaseConfig, BaseModel
from core.langchain_core.pydantic_v1 import create_model as _create_model_base
from core.langchain_core.runnables.schema import StreamEvent

Input = TypeVar("Input", contravariant=True)
# Output type should implement __concat__, as eg str, list, dict do
Output = TypeVar("Output", covariant=True)

async def gated_coro(semaphore: asyncio.Semaphore, coro: Coroutine) -> Any:
    """Run a coroutine with a semaphore.
    Args:
        semaphore: The semaphore to use.
        coro: The coroutine to run.

    Returns:
        The result of the coroutine.
    """
    async with semaphore:
        return await coro


async def gather_with_concurrency(n: Union[int, None], *coros: Coroutine)-> list:
    """Gather coroutines with a limit on the number of concurrent coroutines.

    Args:
        n: The number of coroutines to run concurrently.
        coros: The coroutines to run.

    Returns:
        The results of the coroutines.
    """

    if n is None:
        return await asyncio.gather(*coros)

    semaphore = asyncio.Semaphore(n)

    return await asyncio.gather(*(gated_coro(semaphore, c) for c in coros))

def accepts_run_manager(callable: Callable[..., Any]) -> bool:
    """Check if a callable acceopts a run_manager argumment."""
    try:
        return signature(callable).parameters.get("run_manager") is not None
    except ValueError:
        return False

def accepts_config(callable: Callable[..., Any]) -> bool:
    """Check if a callable accepts a config argument."""
    try:
        return signature(callable).parameters.get("config") is not None
    except ValueError:
        return False

def accepts_context(callable: Callable[..., Any]) -> bool:
    """Check if  a callable accepts a context argument."""
    try:
        return signature(callable).parameters.get("context") is not None
    except ValueError:
        return False

















