from __future__ import annotations


class FailedTestError(Exception):
    """Custom exception raised when a test fails."""

    def __init__(self, message: str, original_error: Exception | None = None) -> None:  # noqa: D107
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

class AppRefreshFailureError(Exception):
    """Custom exception raised when an app refresh operation fails."""

    def __init__(self, message: str, original_error: Exception | None = None) -> None:  # noqa: D107
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class ContextSwitchingFailureError(Exception):
    """Custom exception raised when an context switching operation fails."""

    def __init__(self, message: str, original_error: Exception | None = None) -> None:  # noqa: D107
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class ScreenshotFailureError(Exception):
    """Custom exception raised when a screenshot operation fails."""

    def __init__(self, message: str, original_error: Exception | None = None) -> None:  # noqa: D107
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)
