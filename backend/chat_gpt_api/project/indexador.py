from django.conf import settings
import tiktoken
import openai

import redis
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)
from redis.commands.search.query import Query
from redis.commands.search.field import (
    TextField,
    VectorField
)



class IndexadorDeDocumentos:
    def __init__(self) -> None:
        pass

    