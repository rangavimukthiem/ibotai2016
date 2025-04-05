class MyAppException(Exception):
    """Custom exception for application-specific errors."""

    def __init__(self, error: str = "Application error", code: int = None):
        super().__init__(error)
        self.error = error
        self.code = code

    def __str__(self):
        return f"[Error {self.code}] {self.error}" if self.code else self.error

    def __repr__(self):
        return f"MyAppException(error={self.error!r}, code={self.code!r})"

