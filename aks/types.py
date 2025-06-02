"""
aks/types.py

Production-grade symbolic type system for AkshayaLang.
Defines AKSType, Number, String, Boolean, and Null types.
"""

from abc import ABC, abstractmethod


class AKSType(ABC):
    """Base class for all AKS runtime symbolic types."""

    @abstractmethod
    def type_name(self) -> str:
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class AKSNumber(AKSType):
    def __init__(self, value: float):
        self.value = value

    def type_name(self) -> str:
        return "Number"

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, AKSNumber):
            return AKSNumber(self.value + other.value)
        raise TypeError(f"Cannot add {self.type_name()} and {other.type_name()}")

    def __sub__(self, other):
        if isinstance(other, AKSNumber):
            return AKSNumber(self.value - other.value)
        raise TypeError(f"Cannot subtract {self.type_name()} and {other.type_name()}")

    def __mul__(self, other):
        if isinstance(other, AKSNumber):
            return AKSNumber(self.value * other.value)
        raise TypeError(f"Cannot multiply {self.type_name()} and {other.type_name()}")

    def __truediv__(self, other):
        if isinstance(other, AKSNumber):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero")
            return AKSNumber(self.value / other.value)
        raise TypeError(f"Cannot divide {self.type_name()} and {other.type_name()}")


class AKSString(AKSType):
    def __init__(self, value: str):
        self.value = value

    def type_name(self) -> str:
        return "String"

    def __str__(self):
        return self.value

    def __add__(self, other):
        if isinstance(other, AKSString):
            return AKSString(self.value + other.value)
        raise TypeError(f"Cannot concatenate {self.type_name()} and {other.type_name()}")


class AKSBoolean(AKSType):
    def __init__(self, value: bool):
        self.value = value

    def type_name(self) -> str:
        return "Boolean"

    def __str__(self):
        return "true" if self.value else "false"

    def __bool__(self):
        return self.value


class AKSNull(AKSType):
    def type_name(self) -> str:
        return "Null"

    def __str__(self):
        return "null"

    def __eq__(self, other):
        return isinstance(other, AKSNull)