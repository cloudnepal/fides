from fides.api.schemas.masking.masking_secrets import MaskingSecretCache
from fides.api.util.cache import FidesopsRedis, get_cache, get_masking_secret_cache_key


def cache_secret(masking_secret_cache: MaskingSecretCache, request_id: str) -> None:
    cache: FidesopsRedis = get_cache()
    cache.set_with_autoexpire(
        get_masking_secret_cache_key(
            request_id,
            masking_strategy=masking_secret_cache.masking_strategy,
            secret_type=masking_secret_cache.secret_type,
        ),
        FidesopsRedis.encode_obj(masking_secret_cache.secret),
    )


def clear_cache_secrets(request_id: str) -> None:
    cache: FidesopsRedis = get_cache()
    cache.delete_keys_by_prefix(f"id-{request_id}-masking-secret)")


def clear_cache_identities(request_id: str) -> None:
    """Testing helper just removes some cached identities from the Privacy Request for testing.

    Some of our Privacy Request fixtures automatically cache identities -
    """
    cache: FidesopsRedis = get_cache()
    cache.delete_keys_by_prefix(f"id-{request_id}-identity-")
