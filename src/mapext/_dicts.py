"""
Factories retrieved by hashable keys.
"""
from collections.abc import Hashable, Mapping
from typing import TypeVar, Union
from functools import singledispatchmethod, singledispatch

_KT = TypeVar('_KT', bound = Hashable)
_VT = TypeVar('_VT')

@singledispatch
def _check_overlap(map1, other: Mapping) -> None:
    """
    Raises KeyError if keys from another Mapping overlap.
    """
    raise TypeError(f'Unsupported type: {type(other)}')
@_check_overlap.register
def _(map1: None, other: Mapping) -> None:
    pass
@_check_overlap.register
def _(map1: Mapping, other: Mapping) -> None:
    if set(map1.keys()).intersection(other.keys()):
        raise KeyError("Values are immutable for existing keys.")


class FrozenKeys(dict):
    """
    A dictionary class that fixes key-value pairs once set.
    """
    def __setitem__(self, __key: _KT, __value: _VT) -> None:
        """Set self[key] to value."""
        if __key in self:
            raise KeyError("Values are immutable for existing keys.")
        else:
            return super().__setitem__(__key, __value)

    
    def update(self, __m: Union[Mapping, None] = None, **kwargs) -> None:

        _check_overlap(__m, self)
        _check_overlap(kwargs, self)
        _check_overlap(dict() if isinstance(__m, type(None)) else __m, kwargs)

        super().update(__m = __m, **kwargs)
    
    @singledispatchmethod
    def __or__(self, other):
        name = self.__class__.__name__
        raise TypeError(
            f"unsupported operand type(s) for |: '{name}' and '{type(other)}'"
        )
    @__or__.register
    def _(self, other: Mapping):
        _check_overlap(other, self)
        return FrozenKeys(**self, **other)

    @singledispatchmethod
    def __ior__(self, other):
        name = self.__class__.__name__
        raise TypeError(
            f"unsupported operand type(s) for |=: '{name}' and '{type(other)}'"
        )
    @__ior__.register
    def _(self, other: Mapping):
        _check_overlap(other, self)
        self.update(other)

    
    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}({super().__repr__()[1: -1]})"


class KVDecor(FrozenKeys):
    """
    Registers a class or function to a specific key.

    Subclass of FrozenKeys, classes and functions cannot be overwritten
    once assigned to a key.
    """
    def register(self, __key: _KT) -> callable:
        """Decorator method. Set self[__key] to class or function."""
        def _inner(__value: Union[type, callable]) -> Union[type, callable]:
            
            try:
                self.__setitem__(__key, __value)

            except KeyError as e:
                err_msg = f'{__key} already registered to {self[__key]}'
                raise KeyError(err_msg) from None
            
            except Exception:
                raise
            
            return __value
        
        return _inner
