from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)
