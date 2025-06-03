"""
errors.py — AkshayaLang Symbolic Exception System
"""

class AKSError(Exception):
    """Base class for all AkshayaLang-related exceptions."""
    pass


class LexerError(AKSError):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self._format())

    def _format(self):
        location = f" at line {self.line}, column {self.column}" if self.line is not None else ""
        return f"[LexerError{location}] {self.message}"


class ParserError(AKSError):
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(self._format())

    def _format(self):
        location = f" near token '{self.token.value}'" if self.token else ""
        return f"[ParserError{location}] {self.message}"


class AkshayaRuntimeError(AKSError):
    def __init__(self, message):
        super().__init__(f"[RuntimeError] {message}")
