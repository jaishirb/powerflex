class KeyAlreadyExistsException(Exception):
    def __init__(self, *args: object, key: str) -> None:
        super().__init__(key, *args)
        self.key = key
