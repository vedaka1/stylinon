from dataclasses import dataclass


@dataclass
class Cert:
    alg: str
    kty: str
    key: str
