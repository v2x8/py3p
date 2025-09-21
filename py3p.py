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

exports.prepare()
exports.include('exports')
exports.export()
