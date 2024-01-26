"""
Extend class functionality through dynamic aggregation/composition.
"""
### Imports
from collections.abc import Hashable
from mapext._dicts import _KT, KVDecor
from typing import Callable, Union, TypeVar

### Types
_Cls = TypeVar('_Cls')
_VT = Union[Callable, type]


class KVDescriptor:
    """
    Maps args to extensions in a class composition/aggregation. Retrieve
    extensions by calling self._{attribute name} in owner class.
    """
    _kv_ext: 'KVExtensionsRegistry'

    def __init__(self, ext_log: 'KVExtensionsRegistry'):
        self._kv_ext = ext_log
        
    def __set_name__(self, owner: _Cls, name: str) -> None:
        self.ext_name = '_' + name
    
    def __set__(self, obj: _Cls, value: _KT) -> None:
        setattr(obj, self.ext_name, self._kv_ext[value])
        self.value = value
    
    def __get__(self, obj: _Cls, type = None) -> _VT:
        return self.value


class KVExtensionsRegistry(KVDecor):
    """
    Registers classes for use in Composition/Aggregation.
    """
    def __getitem__(self, key: Hashable) -> _Cls:

        try:
            return super().__getitem__(key)

        except KeyError as e:
            raise KeyError(f'{key} is unregistered') from None

        except Exception:
            raise
    
    def build_descriptor(self) -> KVDescriptor:
        """
        Descriptor will map args to extensions in a class composition.
        Retrieve extensions by calling self.__{attribute name} in owner
        class.
        """
        return KVDescriptor(ext_log = self)