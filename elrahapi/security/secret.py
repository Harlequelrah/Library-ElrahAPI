
from random import choice
import secrets
from typing import Optional


ALGORITHMS_KEY_SIZES = {
    "HS256": 32,         # 256 bits
    "HS384": 48,         # 384 bits
    "HS512": 64,         # 512 bits
}
ALGORITHMS = list(ALGORITHMS_KEY_SIZES.keys())

def define_algorithm_and_key(
        secret_key: Optional[str] = None, algorithm: Optional[str] = None
    ):
        if algorithm:
            if secret_key:
                return algorithm, secret_key
            else:
                key_length = ALGORITHMS_KEY_SIZES.get(algorithm.upper())
                return algorithm, secrets.token_hex(key_length)
        else:
            algo = choice(ALGORITHMS)
            key_length = ALGORITHMS_KEY_SIZES.get(algo.upper())
            return algo, secrets.token_hex(key_length)
