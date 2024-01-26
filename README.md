# Introduction
mapext extends dictionaries by using decorators to assign functions and classes to Hashable keys. The library also provides variations to this base concept, including:

- DescriptorMapping: a descriptor class for easy extension of class functionality dependent on input.
- FactoryRegister: a class that maps keys to factory pattern classes.

kv-decor also features a FrozenKeys class, a dictionary that is immutable once a particular key has been assigned a value.