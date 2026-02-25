import hashlib
from urllib.parse import urlencode

from django.core.cache import cache
from django.db.models import Model


# CACHE KEY GENERATOR (DETAIL / RETRIEVE APIs)
def build_cache_key(model: type[Model], pk: int) -> str:
    """
    Build a unique cache key for a single model instance.

    Why:
    - Used for retrieve/detail APIs
    - Prevents cache collision across apps and models

    Example:
        RBACPermission(pk=5)
        → "user:rbacpermission:5"
    """

    # Model and primary key must be provided to ensure uniqueness
    if not model or not pk:
        raise ValueError("Model and pk are required")

    # Format:
    # {app_label}:{model_name_lower}:{primary_key}
    return f"{model._meta.app_label}:{model.__name__.lower()}:{pk}"


# CACHE KEY GENERATOR (LIST APIs)
def build_list_cache_key(model: type[Model], params: dict, version: int = 1) -> str:
    """
    Build a cache key for list APIs.

    Why:
    - List APIs depend on query parameters (pagination, filters, ordering)
    - Different query params must generate different cache keys

    Format:
        {app}:{model}:list:v{version}:{params_hash}

    Example:
        GET /rbac-permission/?limit=10&offset=0
        → "user:rbacpermission:list:v2:9c1f3a"
    """

    # Base key without query parameters
    base = f"{model._meta.app_label}:{model.__name__.lower()}:list:v{version}"

    # If no query params, return base key
    # (useful for simple list APIs)
    if not params:
        return base

    # Sort params to ensure consistent hashing
    # Example:
    # {"limit":10,"offset":0} == {"offset":0,"limit":10}
    encoded = urlencode(sorted(params.items()))

    # Hash query parameters to keep key short and Redis-friendly
    params_hash = hashlib.md5(encoded.encode()).hexdigest()[:8]

    return f"{base}:{params_hash}"


# CACHE VERSIONING UTILITIES
def get_cache_version_key(model: type[Model]) -> str:
    """
    Build cache version key for a model.

    Why:
    - Used to invalidate ALL list caches safely
    - Avoids deleting keys or scanning Redis

    Example:
        "user:rbacpermission:version"
    """
    return f"{model._meta.app_label}:{model.__name__.lower()}:version"


def get_cache_version(model: type[Model]) -> int:
    """
    Get current cache version for a model.

    Behavior:
    - If version does not exist → initialize with 1
    - Version is shared across all workers/services

    Used when:
    - Building list cache keys
    """
    key = get_cache_version_key(model)
    return cache.get_or_set(key, 1)


def bump_cache_version(model: type[Model]):
    """
    Increment cache version to invalidate ALL list caches.

    Call this AFTER:
    - CREATE
    - UPDATE
    - DELETE

    Result:
    - Old list cache keys become obsolete
    - New requests generate fresh cache automatically
    """
    key = get_cache_version_key(model)
    cache.incr(key)


# VERSIONED LIST CACHE KEY (PRODUCTION ENTRY POINT)
def build_versioned_list_cache_key(model: type[Model], params: dict) -> str:
    """
    Build a production-safe cache key for list APIs.

    Flow:
    1. Get current cache version
    2. Build list cache key using that version
    3. Automatically handles invalidation

    This is the function you should use in views.
    """
    version = get_cache_version(model)
    return build_list_cache_key(model, params, version=version)
