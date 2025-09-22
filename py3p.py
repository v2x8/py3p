# -*- coding: utf-8 -*-
from builtins import classmethod, set

class exports:
    _blacklist = set()
    _whitelist = set()
    @classmethod
    def prepare(cls):
        from builtins import id, map, set
        import inspect
        f_globals = inspect.currentframe().f_back.f_globals
        cls._blacklist = set( map( id, f_globals.values() ) )
        cls._whitelist = set()
    @classmethod
    def include(cls, *args):
        from builtins import map, str
        cls._whitelist.update( map(str, args) )
    @classmethod
    def exclude(cls, *args):
        from builtins import id, map
        cls._blacklist.update( map(id, args) )
    @classmethod
    def export(cls):
        from builtins import id
        import inspect
        f_globals = inspect.currentframe().f_back.f_globals
        f_globals['__all__'] = [
            k for k, v in f_globals.items()
            if k in cls._whitelist or id(v) not in cls._blacklist
        ]
        return f_globals['__all__']

class EmptyType:
    __doc__ = 'The type of the Empty singleton.'
    __slots__ = ()
    _instance = None
    def __new__(cls):
        from builtins import object
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    def __bool__(self):
        return False
    def __repr__(self):
        return 'Empty'
    def __reduce__(self):
        return (self.__class__, ())

exports.prepare()
exports.include('exports')

Empty = EmptyType()

exports.export()
