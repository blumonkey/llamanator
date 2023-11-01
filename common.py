from hashlib import md5

"""
Helper methods/constants
"""


def hash_id(s):
    """Hex digest of md5 hash of string."""
    return md5(s.encode("utf-8")).hexdigest()
