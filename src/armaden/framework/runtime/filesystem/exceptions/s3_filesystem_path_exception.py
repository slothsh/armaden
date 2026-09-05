class S3FilesystemPathException(ValueError):
    def __init__(self, path: str) -> None:
        super().__init__(f"Filesystem path contains a traversal segment: {path}")
        self.path: str = path
