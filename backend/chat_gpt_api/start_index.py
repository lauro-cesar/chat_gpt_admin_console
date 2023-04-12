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
import os





REDIS_VECTOR_DB_HOST=  os.environ.get("REDIS_VECTOR_DB_HOST", default="project_redis_vector_db") 
REDIS_VECTOR_DB_PORT=  os.environ.get("REDIS_VECTOR_DB_PORT", default=6379)
REDIS_VECTOR_DB_PASSWORD= os.environ.get("REDIS_VECTOR_DB_PASSWORD", default="")
VECTOR_DB_VECTOR_DIM =  1024
VECTOR_DB_VECTOR_NUMBER = 0                 
VECTOR_DB_INDEX_NAME = "embeddings-index"           
VECTOR_DB_HNSW_INDEX_NAME = f"{VECTOR_DB_INDEX_NAME}_HNSW"
VECTOR_DB_PREFIX = "doc"                            
VECTOR_DB_DISTANCE_METRIC = "COSINE"

text_embedding = VectorField("content_vector",
    "HNSW", {
        "TYPE": "FLOAT32",
        "DIM": VECTOR_DB_VECTOR_DIM,
        "DISTANCE_METRIC": VECTOR_DB_DISTANCE_METRIC,
        "INITIAL_CAP": VECTOR_DB_VECTOR_NUMBER
    }
)
fields = [text_embedding]


redis_client = redis.Redis(
    password=REDIS_VECTOR_DB_PASSWORD,
    port=REDIS_VECTOR_DB_PORT,
    host=REDIS_VECTOR_DB_HOST
)

try:
    redis_client.ft(VECTOR_DB_HNSW_INDEX_NAME).info()
except Exception as e:
    redis_client.ft(VECTOR_DB_HNSW_INDEX_NAME).create_index(fields = fields,definition = IndexDefinition(prefix=[VECTOR_DB_PREFIX], index_type=IndexType.HASH))
 
