class LocalFilesystemPathException(ValueError):
    def __init__(self, path: str) -> None:
        super().__init__(f"Filesystem path is outside the configured root: {path}")
        self.path: str = path
