import hashlib
from enum import Enum
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from attrs import frozen

KNOWN_HASH_ALGORITHMS: Dict[str, Optional[Callable]] = {
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
    "sha1": hashlib.sha1,
    "gomod": None
    # go.sum files use a non-standard hashing algorithm based on multiple uses of sha256 and conversion to base 64
}


class PackageManagers(Enum):
    NPM = "npm"
    PYPI = "pypi"
    GEM = "gem"
    GOMOD = "gomod"
    CARGO = "cargo"
    MAVEN = "maven"


@frozen(eq=True, order=True)
class LockfileDependency:
    name: str
    version: str
    namespace: PackageManagers
    # map from hash algorithm to list of hashes that are ok
    allowed_hashes: Dict[str, List[str]]
    # sometimes the lockfile gives us a resolved URL, sweet
    resolved_url: Optional[List[str]] = None

    def __post_init__(self) -> None:
        for k in self.allowed_hashes.keys():
            assert (
                k in KNOWN_HASH_ALGORITHMS
            ), f"unknown hash type {k} not in {KNOWN_HASH_ALGORITHMS}"
