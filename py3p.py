# -*- coding: utf-8 -*-
from builtins import classmethod, set, staticmethod

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
        return (EmptyType, ())

exports.prepare()
exports.include('exports')

Empty = EmptyType()

class safe:
    @staticmethod
    def __import__(name):
        from builtins import __import__
        from sys import modules
        module = modules.get(name)
        if module is not None:
            del modules[name]
        result = __import__(name)
        if module is not None:
            modules[name] = module
        return result
    @staticmethod
    def isinstance(obj, class_or_tuple):
        from builtins import TypeError, any, object, tuple, type
        from types import UnionType
        if class_or_tuple is type or safe.isinstance(class_or_tuple, type):
            mro = type.__getattribute__( type(obj), '__mro__' )
            return class_or_tuple in mro
        if safe.isinstance(class_or_tuple, tuple):
            return any( safe.isinstance(obj, cls) for cls in class_or_tuple )
        if safe.isinstance(class_or_tuple, UnionType):
            args = object.__getattribute__(class_or_tuple, '__args__')
            return safe.isinstance(obj, args)
        msg = 'isinstance() arg 2 must be a type, a tuple of types, or a union'
        raise TypeError(msg)
    @staticmethod
    def delattr(obj, name):
        from builtins import object, type
        cls = type if safe.isinstance(obj, type) else object
        return cls.__delattr__(obj, name)
    @staticmethod
    def getattr(obj, name, default=Empty):
        from builtins import AttributeError, object, type
        try:
            cls = type if safe.isinstance(obj, type) else object
            return cls.__getattribute__(obj, name)
        except AttributeError:
            if default is not Empty:
                return default
            raise
    @staticmethod
    def hasattr(obj, name):
        from builtins import AttributeError
        try:
            safe.getattr(obj, name)
            return True
        except AttributeError:
            return False
    @staticmethod
    def setattr(obj, name, value):
        from builtins import object, type
        cls = type if safe.isinstance(obj, type) else object
        return cls.__setattr__(obj, name, value)

def pstr(obj, indent=1):
    from builtins import (  ValueError, bytes, dict, float, id, int,
                            len, list, map, set, str, sorted, tuple )
    if safe.isinstance(indent, list | tuple):
        indent = ''.join(indent)
    if not indent:
        indent = ''
    elif safe.isinstance(indent, bytes | float | int | str):
        try:
            indent = float(indent)
        except ValueError:
            pass
        try:
            indent = int(indent)
        except ValueError:
            pass
        else:
            indent = indent * ' '
    elif indent is True:
        indent = '\t'
    else:
        indent = str(indent)
    suffix = ' ' if indent == '' else '\n'
    memo = set()
    def check(obj, cls):
        if len(obj) == 0:
            if ( result := (
                '{}' if cls is dict else
                '[]' if cls is list else
                '()' if cls is tuple else
                'set()' if cls is set else
            None ) ) is not None: return result
        if id(obj) in memo:
            if ( result := (
                '{...}' if cls is dict else
                '[...]' if cls is list else
                '(...)' if cls is tuple else
                'set(...)' if cls is set else
            None ) ) is not None: return result
        memo.add( id(obj) )
    def _pstr(obj):
        if safe.isinstance(obj, dict):
            if ( result := check(obj, dict) ) is not None:
                return result
            def tostr(item):
                k, v = item
                lines = _pstr(v).splitlines()
                value = f'{suffix}{indent}'.join(lines)
                return f'{indent}{k}: {value}'
            data = f',{suffix}'.join( sorted( map( tostr, obj.items() ) ) )
            return f'{{{suffix}{data}{suffix}}}'
        def tostr(item):
            lines = _pstr(item).splitlines()
            value = f'{suffix}{indent}'.join(lines)
            return f'{indent}{value}'
        if safe.isinstance(obj, list):
            if ( result := check(obj, list) ) is not None:
                return result
            data = f',{suffix}'.join( map(tostr, obj) )
            return f'[{suffix}{data}{suffix}]'
        if safe.isinstance(obj, set):
            if ( result := check(obj, set) ) is not None:
                return result
            data = f',{suffix}'.join( sorted( map(tostr, obj) ) )
            return f'{{{suffix}{data}{suffix}}}'
        if safe.isinstance(obj, tuple):
            if ( result := check(obj, tuple) ) is not None:
                return result
            data = f',{suffix}'.join( map(tostr, obj) )
            return f'({suffix}{data}{suffix})'
        return str(obj)
    return _pstr(obj)

exports.export()
