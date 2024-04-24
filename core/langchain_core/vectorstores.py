"""**Vector store** stores embedded data and performs vector search.

One of the most common ways to store and search over unstructured data is to
embed it and store the resulting embedding vectors, and then query the store
and retrieve the data that are 'most similar' to the embedded query.

**Class hierarchy:**

.. code-block::

    VectorStore --> <name>  # Examples: Annoy, FAISS, Milvus

    BaseRetriever --> VectorStoreRetriever --> <name>Retriever  # Example: VespaRetriever

**Main helpers:**

.. code-block::

    Embeddings, Document
"""  # noqa: E501
from __future__ import annotations

import logging
import math
import warnings
from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

from core.langchain_core.embeddings import Embeddings
from core.langchain_core.pydantic_v1 import Field, root_validator
from core.langchain_core.retrievers import BaseRetriever
from core.langchain_core.runnables.config import run_in_executor


class VectorStore(ABC):
    """Interface for vector store."""

    @abstractmethod
    def add_texts