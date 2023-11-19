import hashlib


def getFileHash(path: str) -> str:
    with open(path, mode="rb") as file:
        return hashlib.md5(file.read()).hexdigest()
